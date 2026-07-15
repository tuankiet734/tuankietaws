---
title: "Deploying the Forecast API"
date: 2024-07-07
weight: 1
chapter: false
pre : " <b> 5.6.1. </b> "
---

### 5.6.1. Deploying the Forecast API on AWS Lambda (Container Image)

Because data science and machine learning libraries (`lightgbm`, `pandas`, `scikit-learn`, `psycopg2-binary`) exceed the AWS Lambda deployment package size limit (50MB zipped / 250MB unzipped), we package the source code and model artifacts into a **Docker Container Image**, store it in **Amazon ECR (Elastic Container Registry)**, and deploy it to **AWS Lambda**.

---

#### 1. Containerization & ECR Publishing Steps:

1. **Dockerfile:** Create a `Dockerfile` to set up the Lambda execution runtime:
   ```dockerfile
   FROM public.ecr.aws/lambda/python:3.10

   # Copy python requirements and install packages
   COPY requirements.txt ${LAMBDA_TASK_ROOT}
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy function handler script
   COPY lambda_function.py ${LAMBDA_TASK_ROOT}

   # Launch Lambda handler function
   CMD [ "lambda_function.lambda_handler" ]
   ```

2. **Build Image Locally:**
   ```bash
   # Build the Docker image targetting x86_64 architecture
   docker build --provenance=false -t fashion-demand-predictor:latest .
   ```

3. **Login and Push to AWS ECR:**
   ```bash
   # Authenticate with the ECR Registry
   aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 507221377279.dkr.ecr.ap-southeast-1.amazonaws.com

   # Tag local image to match ECR Repository URI
   docker tag fashion-demand-predictor:latest 507221377279.dkr.ecr.ap-southeast-1.amazonaws.com/fashion-demand-predictor:latest

   # Push to ECR repository
   docker push 507221377279.dkr.ecr.ap-southeast-1.amazonaws.com/fashion-demand-predictor:latest
   ```

---

#### 2. AWS Lambda Function Handler (`lambda_function.py`):

Upon container startup (Cold Start), Lambda downloads the model pickle files from S3 (`/models/`) to local `/tmp` storage and restores the predictor. For each request, the handler queries time-series feature aggregates from `final_daily` on RDS, applies scaling and categorical encoding, and performs real-time demand inference:

```python
import json
import os
import joblib
import pandas as pd
import numpy as np
import boto3

# AWS RDS PostgreSQL credentials
DB_HOST = "training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "fashiondb"
DB_USER = "dbadmin"
DB_PASS = "Tung2004"

S3_BUCKET = "fashion-retail-model-storage"
model = None
scaler = None
encoder = None

# Download and load pickles on Lambda container bootstrap
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
    print("Model objects loaded successfully!")
except Exception as e:
    print(f"Model loading error: {str(e)}")

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
        # 1. Parse JSON payload from API Gateway
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {}) or event
            
        store_id_raw = body.get('store_id', '1')
        sku = body.get('sku', 'SKU_999')
        date_str = body.get('date', '2026-06-24')
        total_discount_avg_req = body.get('total_discount_avg')
        
        # Format store_id to integer
        if isinstance(store_id_raw, str) and 'STORE_' in store_id_raw.upper():
            store_id = int(store_id_raw.upper().replace('STORE_', ''))
        else:
            store_id = int(store_id_raw)
            
        # Parse dates
        date_obj = pd.to_datetime(date_str)
        month = date_obj.month
        day_of_week = date_obj.dayofweek
        day = date_obj.day
        
        # 2. Retrieve precalculated features from the final_daily RDS table
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
            raise ValueError(f"No features found in DB for store_id={store_id} and sku={sku}")
            
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
            
        # Assemble inputs
        inputs = {'store_id': store_id, 'sku': sku, 'month': month, 'day_of_week': day_of_week, 'day': day}
        inputs.update(db_features)
        
        # 3. Categorical Label Encoding
        encoded_inputs = inputs.copy()
        categorical_cols = ['sku', 'size', 'color', 'category', 'sub_category', 'color_type', 'country', 'city']
        for col in categorical_cols:
            if encoder and col in encoder:
                encoded_inputs[col] = safe_label_transform(encoder[col], inputs[col])
                
        # 4. Align features dynamically with the StandardScaler inputs
        feature_cols = list(scaler.feature_names_in_)
        features_df = pd.DataFrame([encoded_inputs])[feature_cols]
        
        # 5. Apply Scaling and Predict
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

#### 3. Provisioning the Lambda Function on AWS Console:

1. Open **AWS Lambda Console** -> **Create function**.
2. Select **Container image**.
3. **Function name:** Enter `FashionDemandForecastAPI`.
4. **Container image URI:** Click **Browse images**, choose the `fashion-demand-predictor` ECR repository, and select the `latest` tag.
5. **Architecture:** Select **x86_64**.
6. **Configuration & Timeout settings:** Go to **Configuration** tab -> **General configuration**:
   * **Memory:** Set to **1024 MB** or **2048 MB** (LightGBM and Pandas require sufficient RAM).
   * **Timeout:** Set to **30 seconds** (to accommodate the database query latency).

---

#### Verification on AWS Console:

![Lambda API](/images/5-Workshop/5.6-Model-api/lambda-api.png)
