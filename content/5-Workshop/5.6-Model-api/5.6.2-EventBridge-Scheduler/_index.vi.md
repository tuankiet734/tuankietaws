---
title: "Tự động hóa Pipeline"
date: 2024-07-07
weight: 2
chapter: false
pre : " <b> 5.6.2. </b> "
---

### 5.6.2. Tự động hóa Pipeline với Amazon EventBridge & Daily Cron Job

Để đảm bảo mô hình luôn cung cấp kết quả dự báo mới nhất dựa trên lượng giao dịch bán lẻ biến động hàng ngày, chúng ta cần thiết lập tiến trình dự báo hàng ngày tự động. 

Quy trình tự động hóa thực hiện việc:
1. Lấy tất cả các cặp cửa hàng (`store_id`) và sản phẩm (`sku`) hoạt động trong ngày gần nhất.
2. Tạo danh sách các ngày dự báo (7 ngày tiếp theo).
3. Gọi API của máy chủ Orchestrator để tính toán và lưu kết quả vào bảng `demand_forecasts` trên RDS PostgreSQL.

---

#### 1. Kịch bản chạy Batch dự báo hàng ngày (`daily_forecast_updater.py`):

Kịch bản này gọi API dự báo theo từng lô (batch) nhỏ để tránh quá tải máy chủ:

```python
import json
import urllib.request
import urllib.error
import datetime
import psycopg2

# Cấu hình kết nối RDS & Lớp 1 API
DB_HOST = "fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "fashiondb"
DB_USER = "dbadmin"
DB_PASS = "Tung2004"

# Địa chỉ API EC2 (Layer 1 Orchestrator)
EC2_API_URL = "http://18.141.158.110/predict/forecast"

def get_active_store_skus():
    """Lấy danh sách các cặp store_id và sku đang hoạt động trong ngày gần nhất."""
    print("Connecting to RDS to get active store-sku combinations...")
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()
    
    # 1. Tìm ngày gần nhất trong bảng final_daily
    cur.execute("SELECT MAX(date) FROM final_daily;")
    latest_date = cur.fetchone()[0]
    print(f"Latest active date: {latest_date}")
    
    # 2. Truy vấn các tổ hợp store_id và sku hoạt động trong ngày đó
    query = """
        SELECT DISTINCT store_id, sku 
        FROM final_daily
        WHERE date = %s;
    """
    cur.execute(query, (latest_date,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    print(f"Found {len(rows)} active store-sku combinations on {latest_date}.")
    return rows

def run_daily_forecast():
    try:
        store_skus = get_active_store_skus()
    except Exception as e:
        print(f"Error fetching store-SKUs: {e}")
        return
        
    if not store_skus:
        print("No active store-sku combinations found.")
        return
        
    # Xác định danh sách ngày dự báo (Dự báo cho 7 ngày tiếp theo)
    today = datetime.date.today()
    forecast_dates = [str(today + datetime.timedelta(days=i)) for i in range(1, 8)]
    print(f"Generating forecast for dates: {forecast_dates}")
    
    # Gom dữ liệu thành payload gọi API
    items = []
    for store_id, sku in store_skus:
        for date_str in forecast_dates:
            items.append({
                "store_id": str(store_id),
                "sku": sku,
                "date": date_str
            })
            
    # Gọi API theo từng lô (batch) nhỏ để tránh quá tải Gateway
    batch_size = 10
    total_items = len(items)
    print(f"Total forecast requests: {total_items}. Processing in batches of {batch_size}...")
    
    success_count = 0
    for i in range(0, total_items, batch_size):
        batch = items[i:i+batch_size]
        payload = {"items": batch}
        
        req = urllib.request.Request(
            EC2_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                res_body = response.read().decode('utf-8')
                res_json = json.loads(res_body)
                if res_json.get("status") == "success":
                    success_count += len(batch)
                    print(f"Batch {i//batch_size + 1} processed successfully. ({success_count}/{total_items})")
                else:
                    print(f"Batch {i//batch_size + 1} failed: {res_json.get('message')}")
        except urllib.error.HTTPError as he:
            print(f"HTTP Error on batch {i//batch_size + 1}: {he.code} - {he.read().decode('utf-8')}")
        except Exception as e:
            print(f"Error on batch {i//batch_size + 1}: {e}")
            
    print(f"\nCompleted! Successfully triggered forecasting for {success_count}/{total_items} items.")

if __name__ == "__main__":
    run_daily_forecast()
```

---

#### 2. Cấu hình lập lịch tự động:

Chúng ta triển khai lập lịch tự động theo 2 phương án chính sau:

##### Phương án 1: Sử dụng AWS Lambda + Amazon EventBridge Scheduler (Môi trường Cloud)
1. Đóng gói mã nguồn `daily_forecast_updater.py` vào một AWS Lambda function đặt tên là `DailyForecastTrigger`.
2. Truy cập **Amazon EventBridge Console** -> **Schedules**.
3. Tạo một schedule mới:
   * **Schedule type:** Recurring schedule.
   * **Schedule pattern:** Cron-based schedule (Ví dụ: `cron(0 1 * * ? *)` chạy lúc 1:00 AM UTC hàng ngày).
   * **Target:** Chọn **AWS Lambda** và liên kết với hàm `DailyForecastTrigger`.

##### Phương án 2: Sử dụng Cron Job trên EC2 (Đơn giản & Tối ưu chi phí dev)
1. SSH vào máy chủ EC2 backend (`18.141.158.110`).
2. Lưu script `daily_forecast_updater.py` trên thư mục máy chủ.
3. Mở cấu hình crontab:
   ```bash
   crontab -e
   ```
4. Thêm rule để chạy kịch bản lúc 2:00 AM hàng ngày:
   ```bash
   0 2 * * * /usr/bin/python3 /home/ubuntu/daily_forecast_updater.py >> /home/ubuntu/daily_forecast.log 2>&1
   ```

---

#### Minh chứng cấu hình EventBridge:

![EventBridge Rule](/images/5-Workshop/5.6-Model-api/eventbridge-schedule.png)

