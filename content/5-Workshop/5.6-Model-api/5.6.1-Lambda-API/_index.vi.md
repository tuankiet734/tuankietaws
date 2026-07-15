---
title: "Triển khai Forecast API"
date: 2024-07-07
weight: 1
chapter: false
pre : " <b> 5.6.1. </b> "
---

### 5.6.1. Triển khai Forecast API trên AWS Lambda (Container Image)

Do dung lượng của các thư viện khoa học dữ liệu và học máy (`lightgbm`, `pandas`, `scikit-learn`, `psycopg2-binary`) vượt quá giới hạn 250MB của AWS Lambda Zip deployment, chúng ta đóng gói mã nguồn và mô hình thành một **Docker Container Image**, lưu trữ trên **Amazon ECR (Elastic Container Registry)** và triển khai lên **AWS Lambda**.

---

#### 1. Đóng gói Container và đẩy lên Amazon ECR:

1. **Dockerfile:** Tạo tệp `Dockerfile` để cấu hình môi trường chạy Lambda:
   ```dockerfile
   FROM public.ecr.aws/lambda/python:3.10

   # Sao chép các tệp yêu cầu thư viện và mã nguồn
   COPY requirements.txt ${LAMBDA_TASK_ROOT}
   RUN pip install --no-cache-dir -r requirements.txt

   # Sao chép mã nguồn hàm xử lý chính
   COPY lambda_function.py ${LAMBDA_TASK_ROOT}

   # Khởi chạy handler của Lambda
   CMD [ "lambda_function.lambda_handler" ]
   ```

2. **Xây dựng Image cục bộ:**
   ```bash
   # Build Docker image cho kiến trúc x86_64
   docker build --provenance=false -t fashion-demand-predictor:latest .
   ```

3. **Đăng nhập và Đẩy lên ECR:**
   ```bash
   # Đăng nhập vào AWS ECR Registry
   aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 507221377279.dkr.ecr.ap-southeast-1.amazonaws.com

   # Gán thẻ (tag) cho image trùng với ECR Repository
   docker tag fashion-demand-predictor:latest 507221377279.dkr.ecr.ap-southeast-1.amazonaws.com/fashion-demand-predictor:latest

   # Đẩy image lên ECR
   docker push 507221377279.dkr.ecr.ap-southeast-1.amazonaws.com/fashion-demand-predictor:latest
   ```

---

#### 2. Mã nguồn Lambda Function (`lambda_function.py`):

Hàm Lambda khi khởi chạy (Cold Start) sẽ tải các tệp `.pkl` từ S3 `/models/` về thư mục `/tmp` cục bộ và khôi phục mô hình. Khi nhận request chứa thông tin `store_id`, `sku` và `date`, hàm kết nối đến cơ sở dữ liệu `training-db` để truy vấn bộ đặc trưng động tương ứng, kết hợp tiền xử lý và trả về lượng dự báo:

```python
import json
import os
import joblib
import pandas as pd
import numpy as np
import boto3

# Thông tin cơ sở dữ liệu RDS PostgreSQL
DB_HOST = "training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "fashiondb"
DB_USER = "dbadmin"
DB_PASS = "Tung2004"

S3_BUCKET = "fashion-retail-model-storage"
model = None
scaler = None
encoder = None

# Tải mô hình từ S3 khi khởi tạo Lambda (Cold Start)
try:
    if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
        s3 = boto3.client('s3')
        local_model_path = '/tmp/lightgbm_demand_model.pkl'
        local_scaler_path = '/tmp/standard_scaler.pkl'
        local_encoder_path = '/tmp/label_encoders.pkl'
        
        s3.download_file(S3_BUCKET, 'models/lightgbm_demand_model.pkl', local_model_path)
        s3.download_file(S3_BUCKET, 'models/standard_scaler.pkl', local_scaler_path)
        s3.download_file(S3_BUCKET, 'models/label_encoders.pkl', local_encoder_path)
    else:
        local_model_path = 'lightgbm_demand_model.pkl'
        local_scaler_path = 'standard_scaler.pkl'
        local_encoder_path = 'label_encoders.pkl'
        
    model = joblib.load(local_model_path)
    scaler = joblib.load(local_scaler_path)
    encoder = joblib.load(local_encoder_path)
    print("Mô hình và bộ tiền xử lý được load thành công!")
except Exception as e:
    print(f"Lỗi load mô hình: {str(e)}")

def safe_label_transform(label_encoder, value):
    classes_list = label_encoder.classes_
    value_str = str(value)
    if value_str in classes_list:
        return int(label_encoder.transform([value_str])[0])
    if value in classes_list:
        return int(label_encoder.transform([value])[0])
    return int(label_encoder.transform([classes_list[0]])[0])

def lambda_handler(event, context):
    try:
        # 1. Trích xuất body từ request API Gateway
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {}) or event
            
        store_id_raw = body.get('store_id', '1')
        sku = body.get('sku', 'SKU_999')
        date_str = body.get('date', '2026-06-24')
        total_discount_avg_req = body.get('total_discount_avg')
        
        # Định dạng store_id sang số nguyên
        if isinstance(store_id_raw, str) and 'STORE_' in store_id_raw.upper():
            store_id = int(store_id_raw.upper().replace('STORE_', ''))
        else:
            store_id = int(store_id_raw)
            
        # Parse thông số ngày
        date_obj = pd.to_datetime(date_str)
        month = date_obj.month
        day_of_week = date_obj.dayofweek
        day = date_obj.day
        
        # 2. Truy vấn bộ đặc trưng từ bảng final_daily trên RDS
        import psycopg2
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS, connect_timeout=3
        )
        cur = conn.cursor()
        query = """
            SELECT 
                product_id, size, color, total_lifespan, s_total_lifespan, 
                sku_store_coverage, product_store_coverage, s_days_active, 
                s_selling_days_count, s_sales_velocity, s2_days_active, 
                s2_selling_days_count, s2_sales_velocity, avg_usd_price, 
                total_discount_avg, lag_1d, lag_7d, rolling_mean_7d, rolling_std_7d, 
                category, sub_category, color_type, country, city, 
                num_distinct_products, num_distinct_skus,
                lag_14d, lag_28d, rolling_mean_14d, rolling_mean_30d, target_encoding_store_sku
            FROM final_daily
            WHERE store_id = %s AND sku = %s
            ORDER BY ABS(date::date - %s::date)
            LIMIT 1
        """
        cur.execute(query, (store_id, sku, date_str))
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if not row:
            raise ValueError(f"Không tìm thấy đặc trưng cho store_id={store_id} và sku={sku}")
            
        db_features = {
            'product_id': int(row[0]), 'size': str(row[1]), 'color': str(row[2]),
            'total_lifespan': float(row[3]), 's_total_lifespan': float(row[4]),
            'sku_store_coverage': float(row[5]), 'product_store_coverage': float(row[6]),
            's_days_active': float(row[7]), 's_selling_days_count': float(row[8]),
            's_sales_velocity': float(row[9]), 's2_days_active': float(row[10]),
            's2_selling_days_count': float(row[11]), 's2_sales_velocity': float(row[12]),
            'avg_usd_price': float(row[13]), 'total_discount_avg': float(row[14]),
            'lag_1d': float(row[15]), 'lag_7d': float(row[16]), 'rolling_mean_7d': float(row[17]),
            'rolling_std_7d': float(row[18]), 'category': str(row[19]), 'sub_category': str(row[20]),
            'color_type': str(row[21]), 'country': str(row[22]), 'city': str(row[23]),
            'num_distinct_products': int(row[24]), 'num_distinct_skus': int(row[25]),
            'lag_14d': float(row[26]) if row[26] is not None else 1.0,
            'lag_28d': float(row[27]) if row[27] is not None else 1.0,
            'rolling_mean_14d': float(row[28]) if row[28] is not None else 1.15,
            'rolling_mean_30d': float(row[29]) if row[29] is not None else 1.15,
            'target_encoding_store_sku': float(row[30]) if row[30] is not None else 1.15
        }
        
        if total_discount_avg_req is not None:
            db_features['total_discount_avg'] = float(total_discount_avg_req)
            
        # Gom các đầu vào lại
        inputs = {'store_id': store_id, 'sku': sku, 'month': month, 'day_of_week': day_of_week, 'day': day}
        inputs.update(db_features)
        
        # 3. Mã hóa biến phân loại
        encoded_inputs = inputs.copy()
        categorical_cols = ['sku', 'size', 'color', 'category', 'sub_category', 'color_type', 'country', 'city']
        for col in categorical_cols:
            if encoder and col in encoder:
                encoded_inputs[col] = safe_label_transform(encoder[col], inputs[col])
                
        # 4. Sắp xếp thứ tự cột tự động dựa theo bộ chuẩn hóa StandardScaler
        feature_cols = list(scaler.feature_names_in_)
        features_df = pd.DataFrame([encoded_inputs])[feature_cols]
        
        # 5. Thực hiện chuẩn hóa StandardScaler và dự báo
        scaled_features = scaler.transform(features_df)
        scaled_features_df = pd.DataFrame(scaled_features, columns=feature_cols)
        
        prediction = model.predict(scaled_features_df)
        predicted_quantity = max(0.0, float(prediction[0]))
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': 'success',
                'predicted_quantity': round(predicted_quantity, 2),
                'input_received': {
                    'store_id': store_id_raw,
                    'sku': sku,
                    'date': date_str
                }
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'status': 'error', 'message': str(e)})
        }
```

---

#### 3. Cấu hình Hàm Lambda trên AWS Console:

1. Truy cập **AWS Lambda Console** -> **Create function**.
2. Chọn **Container image**.
3. **Function name:** Nhập `FashionDemandForecastAPI`.
4. **Container image URI:** Nhấp vào **Browse images**, chọn ECR repository `fashion-demand-predictor` và chọn tag `latest`.
5. **Architecture:** Chọn **x86_64**.
6. **Configuration & Timeout:** Mở tab **Configuration** -> **General configuration**:
   * **Memory:** Đặt **1024 MB** hoặc **2048 MB** (Mô hình và pandas cần đủ RAM để load dữ liệu).
   * **Timeout:** Đặt **30 giây** (Để đảm bảo đủ thời gian thực hiện truy vấn RDS).

---

#### Minh chứng hoạt động của Lambda Function:

![Lambda API](/images/5-Workshop/5.6-Model-api/lambda-api.png)

