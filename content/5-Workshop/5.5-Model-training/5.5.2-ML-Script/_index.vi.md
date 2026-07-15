---
title: "Kịch bản huấn luyện mô hình"
date: 2024-07-07
weight: 2
chapter: false
pre : " <b> 5.5.2. </b> "
---

### 5.5.2. Kịch bản Huấn luyện Mô hình dự báo (Python ML Script)

Mã nguồn Python chạy trên máy chủ thực hiện việc kết nối tới cơ sở dữ liệu `training-db` (hoặc `fashion-rds`), trích xuất bảng đặc trưng `final_daily`, thực hiện tiền xử lý chuẩn hóa dữ liệu, huấn luyện mô hình dự báo chuỗi thời gian sử dụng thuật toán **LightGBM Regressor** với hàm mất mát **Tweedie Loss** (đặc biệt hiệu quả cho dữ liệu lượng bán lẻ lệch cao và nhiều giá trị 0).

---

#### 1. Các bước chuẩn bị trên máy chủ `ML-Forecast-Server`:

1. Kết nối SSH vào máy chủ sử dụng tệp khóa riêng tư:
   ```bash
   ssh -i "Thanh_key.pem" ubuntu@<PUBLIC_IP_ML_SERVER>
   ```
2. Cập nhật hệ điều hành và cài đặt pip:
   ```bash
   sudo apt-get update -y
   sudo apt-get install python3-pip -y
   ```
3. Cài đặt các thư viện Python cần thiết phục vụ pipeline huấn luyện:
   ```bash
   pip install psycopg2-binary pandas numpy lightgbm scikit-learn joblib boto3
   ```
4. Cấu hình thông tin xác thực AWS CLI trên máy chủ để cho phép tải mô hình lên S3:
   ```bash
   aws configure
   # Nhập AWS Access Key ID, AWS Secret Access Key, ap-southeast-1, và json
   ```

---

#### 2. Kịch bản huấn luyện chi tiết (`train.py` / `retrain.py`):

Dưới đây là mã nguồn xử lý tích hợp 34 đặc trưng chuỗi thời gian, áp dụng Tweedie Loss và tự động hóa xuất các file pickle lưu trữ:

```python
import os
import joblib
import psycopg2
import pandas as pd
import numpy as np
import boto3
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import lightgbm as lgb

# 1. Cấu hình kết nối RDS & S3
DB_HOST = "training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "fashiondb"
DB_USER = "dbadmin"
DB_PASS = "Tung2004"

S3_BUCKET_NAME = "fashion-retail-model-storage"  # Bucket lưu trữ mô hình của dự án
AWS_REGION = "ap-southeast-1"

def load_data_from_rds():
    print("Connecting to RDS database...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    # Lấy toàn bộ dữ liệu từ bảng đặc trưng final_daily
    # Liên kết với transactions để lấy nhãn qty thực tế
    query = """
        SELECT 
            f.*, 
            COALESCE(t.daily_quantity, 0) AS daily_quantity
        FROM final_daily f
        LEFT JOIN (
            SELECT 
                CAST(store_id AS integer) AS store_id, 
                sku, 
                DATE(transaction_date) AS date, 
                SUM(quantity) AS daily_quantity
            FROM transactions
            WHERE store_id ~ '^[0-9]+$'
            GROUP BY store_id, sku, DATE(transaction_date)
        ) t ON f.store_id = t.store_id 
           AND f.sku = t.sku 
           AND f.date = t.date;
    """
    print("Fetching training data with joined daily_quantity target from RDS...")
    df = pd.read_sql(query, conn)
    conn.close()
    print(f"Data loaded successfully! Shape: {df.shape}")
    return df

def train_pipeline():
    # Bước 1: Tải dữ liệu
    try:
        data = load_data_from_rds()
    except Exception as e:
        print(f"Error connecting/fetching data from RDS: {e}")
        return
    
    # Bước 2: Trích xuất đặc trưng thời gian
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values('date')
    data['month'] = data['date'].dt.month
    data['day_of_week'] = data['date'].dt.dayofweek
    data['day'] = data['date'].dt.day
    
    # Bước 3: Mã hóa biến phân loại
    cat_cols = ['sku', 'size', 'color', 'category', 'sub_category', 'color_type', 'country', 'city']
    le_dict = {}
    for col in cat_cols:
        if col in data.columns:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col].astype(str))
            le_dict[col] = le
            
    # Bước 4: Chuẩn bị đặc trưng (loại bỏ cột không cần thiết và cột mục tiêu)
    drop_cols = ['date', 'daily_quantity', 'description_en']
    X = data.drop(columns=[c for c in drop_cols if c in data.columns])
    y = data['daily_quantity']
    
    # Chia tập train/test theo thời gian (80% train, 20% test)
    split_idx = int(len(data) * 0.8)
    X_train = X.iloc[:split_idx]
    y_train = y.iloc[:split_idx]
    X_test = X.iloc[split_idx:]
    y_test = y.iloc[split_idx:]
    
    # Bước 5: Chuẩn hóa StandardScaler cho tất cả các đặc trưng đầu vào
    scaler = StandardScaler()
    feature_cols = X_train.columns.tolist()
    
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Chuyển về DataFrame có tên cột để huấn luyện mô hình
    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=feature_cols)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=feature_cols)
    
    # Bước 6: Huấn luyện LightGBM Regressor với Tweedie Loss
    print("Training LightGBM Regressor with Tweedie Loss...")
    model = lgb.LGBMRegressor(
        objective='tweedie',
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=12,
        num_leaves=31,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(
        X_train_scaled_df, y_train,
        eval_set=[(X_test_scaled_df, y_test)],
        callbacks=[lgb.early_stopping(stopping_rounds=50), lgb.log_evaluation(period=100)]
    )
    
    # Đánh giá mô hình
    y_pred = model.predict(X_test_scaled_df)
    y_pred = np.maximum(y_pred, 0)  # Lượng nhu cầu dự báo không thể âm
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / (y_test + 1))) * 100
    
    print("\n--- BÁO CÁO HIỆU NĂNG MÔ HÌNH ---")
    print(f"RMSE (Sai số bình phương trung bình): {rmse:.4f}")
    print(f"MAE (Sai số tuyệt đối trung bình):  {mae:.4f}")
    print(f"R2 Score:                             {r2:.4f}")
    print(f"MAPE (Sai số phần trăm trung bình):  {mape:.2f}%")
    print("--------------------------------")
    
    # Bước 7: Lưu mô hình và các bộ chuyển đổi tiền xử lý ra file cục bộ
    print("Saving pickles locally...")
    joblib.dump(model, "lightgbm_demand_model.pkl")
    joblib.dump(scaler, "standard_scaler.pkl")
    joblib.dump(le_dict, "label_encoders.pkl")
    print("Pickle files saved successfully.")
    
    # Bước 8: Upload lên S3 (Model Storage)
    upload_to_s3()

def upload_to_s3():
    try:
        print("Uploading models to AWS S3 bucket...")
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        
        files_to_upload = ["lightgbm_demand_model.pkl", "standard_scaler.pkl", "label_encoders.pkl"]
        for file in files_to_upload:
            s3_client.upload_file(file, S3_BUCKET_NAME, f"models/{file}")
            print(f"Uploaded {file} successfully to s3://{S3_BUCKET_NAME}/models/{file}")
            
    except Exception as e:
        print(f"\n[WARNING] Lỗi upload S3: {e}")
        print("Mô hình đã được lưu cục bộ thành công.")

if __name__ == "__main__":
    train_pipeline()
```

---

#### 3. Thực thi kịch bản huấn luyện:

Để chạy kịch bản huấn luyện mô hình, thực thi lệnh sau trên terminal của máy chủ EC2:
```bash
python3 train.py
```

Sau khi hoàn tất, màn hình sẽ in ra thông tin đánh giá mô hình và logs xác nhận upload thành công lên S3:
```text
Connecting to RDS database...
Fetching training data with joined daily_quantity target from RDS...
Data loaded successfully! Shape: (109500, 34)
Training LightGBM Regressor with Tweedie Loss...
[100]	valid_0's tweedie: 1.8415
[200]	valid_0's tweedie: 1.8398
Early stopping, best iteration is:
[180]	valid_0's tweedie: 1.8392

--- BÁO CÁO HIỆU NĂNG MÔ HÌNH ---
RMSE (Sai số bình phương trung bình): 0.5184
MAE (Sai số tuyệt đối trung bình):  0.2984
R2 Score:                             0.0971
MAPE (Sai số phần trăm trung bình):  11.47%
--------------------------------
Saving pickles locally...
Pickle files saved successfully.
Uploading models to AWS S3 bucket...
Uploaded lightgbm_demand_model.pkl successfully to s3://fashion-retail-model-storage/models/lightgbm_demand_model.pkl
Uploaded standard_scaler.pkl successfully to s3://fashion-retail-model-storage/models/standard_scaler.pkl
Uploaded label_encoders.pkl successfully to s3://fashion-retail-model-storage/models/label_encoders.pkl
```

