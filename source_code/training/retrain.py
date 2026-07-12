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
DB_HOST = "fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "fashiondb"
DB_USER = "dbadmin"
DB_PASS = "Tung2004"

# Thường Bucket S3 lưu trữ mô hình của dự án
S3_BUCKET_NAME = "fashion-retail-model-storage"  
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
            
    # Bước 4: Chuẩn bị đặc trưng
    drop_cols = ['date', 'daily_quantity', 'description_en']
    X = data.drop(columns=[c for c in drop_cols if c in data.columns])
    y = data['daily_quantity']
    
    # Chia tập train/test theo thời gian (80% train, 20% test)
    split_idx = int(len(data) * 0.8)
    X_train = X.iloc[:split_idx]
    y_train = y.iloc[:split_idx]
    X_test = X.iloc[split_idx:]
    y_test = y.iloc[split_idx:]
    
    # Bước 5: Chuẩn hóa StandardScaler
    scaler = StandardScaler()
    feature_cols = X_train.columns.tolist()
    
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Chuyển về DataFrame có tên cột để tránh Warning từ LightGBM
    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=feature_cols)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=feature_cols)
    
    # Bước 6: Huấn luyện LightGBM
    print("Training LightGBM Regressor...")
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
    y_pred = np.maximum(y_pred, 0)  # Demand không thể âm
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / (y_test + 1))) * 100
    
    print("\n--- MODEL PERFORMANCE REPORT ---")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE:  {mae:.4f}")
    print(f"R2:   {r2:.4f}")
    print(f"MAPE: {mape:.2f}%")
    print("--------------------------------")
    
    # Bước 7: Lưu mô hình và tiền xử lý ra file cục bộ
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
        
        # Kiểm tra xem bucket có tồn tại hay không trước khi upload
        # Nếu chưa cấu hình credentials hoặc bucket chưa tạo, phần này sẽ báo lỗi
        files_to_upload = ["lightgbm_demand_model.pkl", "standard_scaler.pkl", "label_encoders.pkl"]
        for file in files_to_upload:
            s3_client.upload_file(file, S3_BUCKET_NAME, f"models/{file}")
            print(f"Uploaded {file} successfully to s3://{S3_BUCKET_NAME}/models/{file}")
            
    except Exception as e:
        print(f"\n[WARNING] Error uploading to S3: {e}")
        print("Model files were successfully saved locally.")
        print("Please ensure S3 Bucket exists and AWS CLI credentials are set up for automatic upload.")

if __name__ == "__main__":
    train_pipeline()
