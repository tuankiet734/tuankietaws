---
title: "LightGBM Training Script"
date: 2024-07-07
weight: 2
chapter: false
pre : " <b> 5.5.2. </b> "
---

### 5.5.2. Machine Learning Training Script (Python ML Script)

A Python script runs on the EC2 machine, connecting to the `training-db` (or `fashion-rds`) database, downloading feature records from the `final_daily` table, pre-processing features using standard scaling and label encoding, and training a **LightGBM Regressor** model using **Tweedie Loss** (which handles zero-inflated and highly skewed retail sales data exceptionally well).

---

#### 1. Server Environment Setup on `ML-Forecast-Server`:

1. Establish SSH connection using your private key:
   ```bash
   ssh -i "Thanh_key.pem" ubuntu@<PUBLIC_IP_ML_SERVER>
   ```
2. Update packages and install python-pip:
   ```bash
   sudo apt-get update -y
   sudo apt-get install python3-pip -y
   ```
3. Install the required Python packages for the training pipeline:
   ```bash
   pip install psycopg2-binary pandas numpy lightgbm scikit-learn joblib boto3
   ```
4. Configure AWS CLI credentials to allow uploading model artifacts to S3:
   ```bash
   aws configure
   # Enter AWS Access Key ID, AWS Secret Access Key, ap-southeast-1, and json
   ```

---

#### 2. Model Training Script (`train.py` / `retrain.py`):

Below is the complete Python pipeline integrating all 34 time-series features and outputting model pickles:

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

# 1. RDS & S3 Configuration
DB_HOST = "training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "fashiondb"
DB_USER = "dbadmin"
DB_PASS = "Tung2004"

S3_BUCKET_NAME = "fashion-retail-model-storage"  # S3 bucket for model storage
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
    # Query features from final_daily and join with transactions to get the target labels
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
    # Step 1: Load training dataset
    try:
        data = load_data_from_rds()
    except Exception as e:
        print(f"Error connecting/fetching data from RDS: {e}")
        return
    
    # Step 2: Time features extraction
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values('date')
    data['month'] = data['date'].dt.month
    data['day_of_week'] = data['date'].dt.dayofweek
    data['day'] = data['date'].dt.day
    
    # Step 3: Categorical Label Encoding
    cat_cols = ['sku', 'size', 'color', 'category', 'sub_category', 'color_type', 'country', 'city']
    le_dict = {}
    for col in cat_cols:
        if col in data.columns:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col].astype(str))
            le_dict[col] = le
            
    # Step 4: Drop metadata fields
    drop_cols = ['date', 'daily_quantity', 'description_en']
    X = data.drop(columns=[c for c in drop_cols if c in data.columns])
    y = data['daily_quantity']
    
    # Chronological Train-Test Split (80% Train, 20% Test)
    split_idx = int(len(data) * 0.8)
    X_train = X.iloc[:split_idx]
    y_train = y.iloc[:split_idx]
    X_test = X.iloc[split_idx:]
    y_test = y.iloc[split_idx:]
    
    # Step 5: Feature Scaling
    scaler = StandardScaler()
    feature_cols = X_train.columns.tolist()
    
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create DataFrames with column names to avoid warnings
    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=feature_cols)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=feature_cols)
    
    # Step 6: Train LightGBM Regressor with Tweedie Loss
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
    
    # Evaluate performance
    y_pred = model.predict(X_test_scaled_df)
    y_pred = np.maximum(y_pred, 0)  # Demand cannot be negative
    
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
    
    # Step 7: Export model and processors locally
    print("Saving pickles locally...")
    joblib.dump(model, "lightgbm_demand_model.pkl")
    joblib.dump(scaler, "standard_scaler.pkl")
    joblib.dump(le_dict, "label_encoders.pkl")
    print("Pickle files saved successfully.")
    
    # Step 8: Upload to S3
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
        print(f"\n[WARNING] S3 Upload Error: {e}")
        print("Model pickles were successfully saved locally.")

if __name__ == "__main__":
    train_pipeline()
```

---

#### 3. Execution:

Run the script from your EC2 CLI:
```bash
python3 train.py
```

The CLI prints the evaluations and S3 upload receipts:
```text
Connecting to RDS database...
Fetching training data with joined daily_quantity target from RDS...
Data loaded successfully! Shape: (109500, 34)
Training LightGBM Regressor with Tweedie Loss...
[100]	valid_0's tweedie: 1.8415
[200]	valid_0's tweedie: 1.8398
Early stopping, best iteration is:
[180]	valid_0's tweedie: 1.8392

--- MODEL PERFORMANCE REPORT ---
RMSE: 0.5184
MAE:  0.2984
R2:   0.0971
MAPE: 11.47%
--------------------------------
Saving pickles locally...
Pickle files saved successfully.
Uploading models to AWS S3 bucket...
Uploaded lightgbm_demand_model.pkl successfully to s3://fashion-retail-model-storage/models/lightgbm_demand_model.pkl
Uploaded standard_scaler.pkl successfully to s3://fashion-retail-model-storage/models/standard_scaler.pkl
Uploaded label_encoders.pkl successfully to s3://fashion-retail-model-storage/models/label_encoders.pkl
```

