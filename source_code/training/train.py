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
DB_HOST_FASHION = "fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
DB_HOST_TRAINING = "training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "fashiondb"
DB_USER = "dbadmin"
DB_PASS = "Tung2004"

S3_BUCKET_NAME = "fashion-product-images-group3979"  
AWS_REGION = "ap-southeast-1"

def load_data_from_rds():
    # Bước a: Lấy transactions từ database fashion-rds
    print(f"1. Connecting to fashion-rds database at {DB_HOST_FASHION} to get transactions...")
    conn_fashion = psycopg2.connect(
        host=DB_HOST_FASHION,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    trans_query = """
        SELECT 
            CAST(store_id AS integer) AS store_id, 
            sku, 
            DATE(transaction_date) AS date, 
            SUM(quantity) AS daily_quantity
        FROM transactions
        WHERE store_id ~ '^[0-9]+$'
        GROUP BY store_id, sku, DATE(transaction_date);
    """
    df_trans = pd.read_sql(trans_query, conn_fashion)
    conn_fashion.close()
    print(f"Transactions data loaded! Shape: {df_trans.shape}")
    
    # Bước b: Lấy final_daily từ database training-db
    print(f"2. Connecting to training-db database at {DB_HOST_TRAINING} to get features...")
    conn_training = psycopg2.connect(
        host=DB_HOST_TRAINING,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    features_query = "SELECT * FROM final_daily;"
    df_features = pd.read_sql(features_query, conn_training)
    conn_training.close()
    print(f"Features data loaded! Shape: {df_features.shape}")
    
    # Bước c: Thực hiện LEFT JOIN bằng Pandas ngay trong bộ nhớ để tránh rò rỉ đặc trưng
    print("3. Merging transactions and features in memory via Pandas...")
    df_features['date'] = pd.to_datetime(df_features['date'])
    df_trans['date'] = pd.to_datetime(df_trans['date'])
    
    df = pd.merge(df_features, df_trans, on=['store_id', 'sku', 'date'], how='left')
    df['qty'] = df['daily_quantity'].fillna(0)
    df.drop(columns=['daily_quantity'], inplace=True, errors='ignore')
    
    print(f"Dataset ready for training! Shape: {df.shape}")
    return df

def train_pipeline():
    # Bước 1: Tải dữ liệu từ RDS
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
    drop_cols = ['date', 'qty', 'description_en']
    X = data.drop(columns=[c for c in drop_cols if c in data.columns])
    y = data['qty']
    
    # Chia tập train/validation theo thời gian (80% train, 20% validation)
    split_idx = int(len(data) * 0.8)
    X_train = X.iloc[:split_idx]
    y_train = y.iloc[:split_idx]
    X_val = X.iloc[split_idx:]
    y_val = y.iloc[split_idx:]
    
    # Bước 5: Chuẩn hóa StandardScaler cho đặc trưng số
    # Xác định các cột số (loại trừ các cột phân loại đã mã hóa và ID)
    non_numeric_cols = cat_cols + ['store_id', 'product_id', 'month', 'day_of_week', 'day']
    num_cols = [c for c in X_train.columns if c not in non_numeric_cols]
    
    scaler = StandardScaler()
    feature_cols = X_train.columns.tolist()
    
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    
    # Chuyển về DataFrame để tránh Warning từ LightGBM
    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=feature_cols)
    X_val_scaled_df = pd.DataFrame(X_val_scaled, columns=feature_cols)
    
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
        eval_set=[(X_val_scaled_df, y_val)],
        callbacks=[lgb.early_stopping(stopping_rounds=50), lgb.log_evaluation(period=100)]
    )
    
    # Đánh giá mô hình
    y_pred = model.predict(X_val_scaled_df)
    y_pred = np.maximum(y_pred, 0)  # Demand không thể âm
    
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    mae = mean_absolute_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)
    mape = np.mean(np.abs((y_val - y_pred) / (y_val + 1))) * 100
    
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
        print(f"Uploading models to AWS S3 bucket s3://{S3_BUCKET_NAME}/models/ ...")
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        
        files_to_upload = ["lightgbm_demand_model.pkl", "standard_scaler.pkl", "label_encoders.pkl"]
        for file in files_to_upload:
            s3_client.upload_file(file, S3_BUCKET_NAME, f"models/{file}")
            print(f"Uploaded {file} successfully to s3://{S3_BUCKET_NAME}/models/{file}")
            
    except Exception as e:
        print(f"\n[WARNING] Error uploading to S3: {e}")
        print("Model files were successfully saved locally.")

if __name__ == "__main__":
    train_pipeline()
