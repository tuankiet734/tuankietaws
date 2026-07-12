import os
import json
import datetime
import logging
import joblib
import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extras import execute_values
import boto3
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel, Field, validator
from typing import Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("lambda_app")

# 1. Cấu hình RDS & S3
DB_HOST = "training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "fashiondb"
DB_USER = "dbadmin"
DB_PASS = "Tung2004"

S3_BUCKET = "fashion-product-images-group3979"
MODEL_VERSION = "lgbm_v1"

# Required features in correct column order (default list)
FEATURE_COLS = [
    'store_id', 'product_id', 'sku', 'size', 'color', 
    'total_lifespan', 's_total_lifespan', 'sku_store_coverage', 'product_store_coverage', 
    's_days_active', 's_selling_days_count', 's_sales_velocity', 
    's2_days_active', 's2_selling_days_count', 's2_sales_velocity', 
    'avg_usd_price', 'total_discount_avg', 'lag_1d', 'lag_7d', 
    'rolling_mean_7d', 'rolling_std_7d', 'category', 'sub_category', 
    'color_type', 'country', 'city', 'num_distinct_products', 'num_distinct_skus', 
    'month', 'day_of_week', 'day'
]

# ==========================================
# 2. COLD START LOGIC - DOWNLOAD MODELS FROM S3
# ==========================================
model = None
scaler = None
encoder = None

def download_and_load_models():
    global model, scaler, encoder, FEATURE_COLS
    
    # Paths in Lambda writable /tmp directory
    tmp_model_path = '/tmp/lightgbm_demand_model.pkl'
    tmp_scaler_path = '/tmp/standard_scaler.pkl'
    tmp_encoder_path = '/tmp/label_encoders.pkl'
    
    try:
        # Check if running in AWS Lambda
        if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
            logger.info("Running in AWS Lambda. Downloading model files from S3...")
            s3 = boto3.client('s3')
            s3.download_file(S3_BUCKET, 'models/lightgbm_demand_model.pkl', tmp_model_path)
            s3.download_file(S3_BUCKET, 'models/standard_scaler.pkl', tmp_scaler_path)
            s3.download_file(S3_BUCKET, 'models/label_encoders.pkl', tmp_encoder_path)
        else:
            logger.info("Running locally. Using local model files...")
            tmp_model_path = 'lightgbm_demand_model.pkl'
            tmp_scaler_path = 'standard_scaler.pkl'
            tmp_encoder_path = 'label_encoders.pkl'
            
        # Load pickles into memory
        model = joblib.load(tmp_model_path)
        scaler = joblib.load(tmp_scaler_path)
        encoder = joblib.load(tmp_encoder_path)
        
        # Dynamically align FEATURE_COLS with the fitted features of the scaler
        if hasattr(scaler, 'feature_names_in_'):
            FEATURE_COLS = list(scaler.feature_names_in_)
            print("Aligned FEATURE_COLS with scaler fitted features (count):", len(FEATURE_COLS))
            print("Scaler fitted features list:", FEATURE_COLS)
        else:
            print("Scaler has NO feature_names_in_ attribute at startup")
            
        print("All model components successfully loaded into memory!")
    except Exception as e:
        logger.error(f"Error loading models during cold start: {e}")
        # If running locally and files do not exist yet, we allow startup to verify endpoints
        if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
            raise e

# Function will be triggered at the end of module definition

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def safe_label_transform(label_encoder, value):
    classes_list = label_encoder.classes_
    # If the encoder classes are strings
    if len(classes_list) > 0 and isinstance(classes_list[0], str):
        value_str = str(value)
        if value_str in classes_list:
            return int(label_encoder.transform([value_str])[0])
    if value in classes_list:
        return int(label_encoder.transform([value])[0])
    # Fallback to the first class if label is unseen
    fallback_val = classes_list[0]
    return int(label_encoder.transform([fallback_val])[0])

# FEATURE_COLS is defined at the top and aligned dynamically during download_and_load_models()

# ==========================================
# 4. CORE INFERENCE & DATABASE UPDATER LOGIC
# ==========================================
def run_daily_forecasting_logic():
    if model is None or scaler is None or encoder is None:
        raise ValueError("Model components are not loaded on the server.")

    conn = get_db_connection()
    cur = conn.cursor()
    
    # a. Tìm ngày gần nhất trong bảng final_daily
    logger.info("Finding the latest date in final_daily...")
    cur.execute("SELECT MAX(date) FROM final_daily;")
    latest_date_row = cur.fetchone()
    if not latest_date_row or not latest_date_row[0]:
        cur.close()
        conn.close()
        raise ValueError("The final_daily table is empty or does not contain valid dates.")
    
    latest_date = latest_date_row[0]
    logger.info(f"Latest active date found: {latest_date}")
    
    # b. Lấy toàn bộ đặc trưng của ngày gần nhất
    logger.info(f"Retrieving features for date: {latest_date}...")
    query = """
        SELECT 
            store_id, sku, product_id, size, color, 
            total_lifespan, s_total_lifespan, sku_store_coverage, product_store_coverage, 
            s_days_active, s_selling_days_count, s_sales_velocity, 
            s2_days_active, s2_selling_days_count, s2_sales_velocity, 
            avg_usd_price, total_discount_avg, lag_1d, lag_7d, 
            rolling_mean_7d, rolling_std_7d, category, sub_category, 
            color_type, country, city, num_distinct_products, num_distinct_skus,
            lag_14d, lag_28d, rolling_mean_14d, rolling_mean_30d, target_encoding_store_sku
        FROM final_daily
        WHERE date = %s;
    """
    df_features = pd.read_sql(query, conn, params=[latest_date])
    if df_features.empty:
        cur.close()
        conn.close()
        raise ValueError(f"No features found in final_daily for date {latest_date}.")
        
    logger.info(f"Fetched {len(df_features)} store-sku features.")
    
    # c. Sinh dự báo cho 7 ngày kế tiếp
    # Xác định danh sách ngày dự báo (7 ngày tiếp theo tính từ ngày hiện tại)
    today = datetime.date.today()
    forecast_dates = [today + datetime.timedelta(days=i) for i in range(1, 8)]
    logger.info(f"Generating forecasts for dates: {[str(d) for d in forecast_dates]}")
    
    # Nhân bản dataframe đặc trưng cho 7 ngày dự báo và thêm cột ngày tương ứng
    list_dfs = []
    for d in forecast_dates:
        temp_df = df_features.copy()
        temp_df['date'] = d
        temp_df['month'] = d.month
        temp_df['day_of_week'] = d.weekday()  # Monday=0, Sunday=6
        temp_df['day'] = d.day
        list_dfs.append(temp_df)
        
    df_all_dates = pd.concat(list_dfs, ignore_index=True)
    
    # d. Tiền xử lý dữ liệu đặc trưng bằng label encoders và scaler
    logger.info("Preprocessing features for LightGBM model...")
    cat_cols = ['sku', 'size', 'color', 'category', 'sub_category', 'color_type', 'country', 'city']
    
    # Áp dụng mã hóa LabelEncoder
    for col in cat_cols:
        if col in df_all_dates.columns and col in encoder:
            le = encoder[col]
            # Tối ưu hóa: Sử dụng dictionary mapping thay vì gọi transform từng dòng để tránh timeout
            mapping_dict = {str(cls): idx for idx, cls in enumerate(le.classes_)}
            df_all_dates[col] = df_all_dates[col].astype(str).map(mapping_dict).fillna(0).astype(int)
            
    # Sắp xếp các cột theo đúng thứ tự huấn luyện
    print("df_all_dates columns:", list(df_all_dates.columns))
    print("FEATURE_COLS:", FEATURE_COLS)
    if hasattr(scaler, 'feature_names_in_'):
        print("scaler.feature_names_in_:", list(scaler.feature_names_in_))
    else:
        print("scaler does NOT have feature_names_in_")
        
    X = df_all_dates[FEATURE_COLS]
    
    # Chuẩn hóa đặc trưng bằng StandardScaler
    X_scaled = scaler.transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=FEATURE_COLS)
    
    # e. Chạy dự báo mô hình
    logger.info("Running predictions with LightGBM Regressor...")
    predictions = model.predict(X_scaled_df)
    predictions = np.maximum(predictions, 0)  # Demand không thể âm
    df_all_dates['pred_qty'] = predictions
    
    # f. Gom nhóm dự báo theo tuần: (store_id, sku, product_id, year, week)
    logger.info("Aggregating daily predictions to weekly forecasts...")
    df_all_dates['year'] = df_all_dates['date'].apply(lambda d: int(d.year))
    df_all_dates['week'] = df_all_dates['date'].apply(lambda d: int(d.isocalendar()[1]))
    
    # Group by weekly keys and sum the predictions
    weekly_agg = df_all_dates.groupby(['store_id', 'sku', 'product_id', 'year', 'week'])['pred_qty'].sum().reset_index()
    logger.info(f"Aggregated into {len(weekly_agg)} weekly forecasts.")
    
    # g. Thực hiện ghi kết quả hàng loạt (bulk insert) vào bảng demand_forecasts
    logger.info("Writing forecast results to demand_forecasts table in database...")
    try:
        # Tập hợp các năm-tuần duy nhất cần ghi đè để dọn dẹp trước khi nạp mới (tránh trùng lặp dữ liệu)
        unique_weeks = weekly_agg[['year', 'week']].drop_duplicates().values.tolist()
        
        # Bắt đầu giao dịch (transaction)
        for yr, wk in unique_weeks:
            cur.execute(
                "DELETE FROM demand_forecasts WHERE forecast_year = %s AND forecast_week = %s AND model_version = %s;",
                (int(yr), int(wk), MODEL_VERSION)
            )
        
        # Chuẩn bị dữ liệu ghi hàng loạt
        insert_records = []
        for _, row in weekly_agg.iterrows():
            insert_records.append((
                str(row['store_id']),
                str(row['sku']),
                str(row['product_id']),
                int(row['year']),
                int(row['week']),
                float(row['pred_qty']),
                MODEL_VERSION
            ))
            
        insert_query = """
            INSERT INTO demand_forecasts (store_id, sku, product_id, forecast_year, forecast_week, predicted_quantity, model_version)
            VALUES %s;
        """
        
        # Chạy bulk insert dùng execute_values (siêu nhanh)
        execute_values(cur, insert_query, insert_records)
        
        # Commit giao dịch nếu không có lỗi
        conn.commit()
        logger.info("Successfully saved all weekly forecasts to RDS database!")
        
        result_summary = {
            "forecast_date_range": [str(d) for d in forecast_dates],
            "total_inserted_records": len(insert_records),
            "affected_weeks": [{"year": int(yr), "week": int(wk)} for yr, wk in unique_weeks]
        }
    except Exception as db_ex:
        conn.rollback()
        logger.error(f"Database error during bulk insert. Transaction rolled back: {db_ex}")
        raise db_ex
    finally:
        cur.close()
        conn.close()
        
    return result_summary

# ==========================================
# 5. FASTAPI APPLICATION ENDPOINTS
# ==========================================
class PredictRequest(BaseModel):
    store_id: str = Field(..., description="ID of the store (e.g., '1', 'STORE_001')", example="1")
    sku: str = Field(..., description="SKU code of the product (e.g., 'CHAC10010--')", example="CHAC10010--")
    date: str = Field(..., description="Target prediction date in YYYY-MM-DD format", example="2026-06-24")
    total_discount_avg: Optional[float] = Field(None, description="Optional override for discount average (0.0 to 1.0)", example=0.15)

    @validator('date')
    def validate_date_format(cls, v):
        try:
            datetime.datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        return v

    @validator('total_discount_avg')
    def validate_discount(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError("Discount average must be between 0.0 and 1.0")
        return v

app = FastAPI(
    title="Fashion Retail Demand Forecasting - AWS Lambda Model API",
    description="Automated ML Inference pipeline running on AWS Lambda with EventBridge scheduler.",
    version="1.0.0"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "encoder_loaded": encoder is not None
    }

@app.post("/predict", status_code=status.HTTP_200_OK)
def predict_endpoint(req: PredictRequest):
    try:
        # Parse store_id to integer
        store_id_raw = req.store_id
        if 'STORE_' in store_id_raw.upper():
            store_id = int(store_id_raw.upper().replace('STORE_', ''))
        else:
            try:
                store_id = int(store_id_raw)
            except ValueError:
                store_id = 1
                
        sku = req.sku
        date_str = req.date
        total_discount_avg_req = req.total_discount_avg
        
        # Parse date
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        month = date_obj.month
        day_of_week = date_obj.weekday()
        day = date_obj.day
        
        # Fetch features from RDS
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            query = """
                SELECT 
                    product_id, size, color, total_lifespan, s_total_lifespan, 
                    sku_store_coverage, product_store_coverage, s_days_active, 
                    s_selling_days_count, s_sales_velocity, s2_days_active, 
                    s2_selling_days_count, s2_sales_velocity, avg_usd_price, 
                    total_discount_avg, lag_1d, lag_7d, rolling_mean_7d, rolling_std_7d, 
                    category, sub_category, color_type, country, city, 
                    num_distinct_products, num_distinct_skus
                FROM final_daily
                WHERE store_id = %s AND sku = %s
                ORDER BY ABS(date::date - %s::date)
                LIMIT 1
            """
            cur.execute(query, (store_id, sku, date_str))
            row = cur.fetchone()
            cur.close()
            conn.close()
        except Exception as db_err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database connection error: {str(db_err)}"
            )
            
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No features found in DB for store_id={store_id_raw} and sku={sku}"
            )
            
        # Parse features
        db_features = {
            'product_id': int(row[0]),
            'size': str(row[1]),
            'color': str(row[2]),
            'total_lifespan': float(row[3]),
            's_total_lifespan': float(row[4]),
            'sku_store_coverage': float(row[5]),
            'product_store_coverage': float(row[6]),
            's_days_active': float(row[7]),
            's_selling_days_count': float(row[8]),
            's_sales_velocity': float(row[9]),
            's2_days_active': float(row[10]),
            's2_selling_days_count': float(row[11]),
            's2_sales_velocity': float(row[12]),
            'avg_usd_price': float(row[13]),
            'total_discount_avg': float(row[14]),
            'lag_1d': float(row[15]),
            'lag_7d': float(row[16]),
            'rolling_mean_7d': float(row[17]),
            'rolling_std_7d': float(row[18]),
            'category': str(row[19]),
            'sub_category': str(row[20]),
            'color_type': str(row[21]),
            'country': str(row[22]),
            'city': str(row[23]),
            'num_distinct_products': int(row[24]),
            'num_distinct_skus': int(row[25])
        }
        
        # Override discount if passed in request
        if total_discount_avg_req is not None:
            db_features['total_discount_avg'] = float(total_discount_avg_req)
            
        # Assemble inputs
        inputs = {
            'store_id': store_id,
            'sku': sku,
            'month': month,
            'day_of_week': day_of_week,
            'day': day
        }
        inputs.update(db_features)
        
        # Categorical Encoding
        encoded_inputs = inputs.copy()
        categorical_cols = ['sku', 'size', 'color', 'category', 'sub_category', 'color_type', 'country', 'city']
        for col in categorical_cols:
            if encoder and col in encoder:
                encoded_inputs[col] = safe_label_transform(encoder[col], inputs[col])
                
        # Scale and Predict
        features_df = pd.DataFrame([encoded_inputs])[FEATURE_COLS]
        scaled_features = scaler.transform(features_df)
        scaled_features_df = pd.DataFrame(scaled_features, columns=FEATURE_COLS)
        
        prediction = model.predict(scaled_features_df)
        predicted_quantity = float(prediction[0])
        predicted_quantity = max(0.0, predicted_quantity)
        
        return {
            'status': 'success',
            'message': 'Dự báo thành công (Mô hình LightGBM thật)',
            'input_received': {
                'store_id': store_id_raw,
                'sku': sku,
                'date': date_str,
                'total_discount_avg': total_discount_avg_req
            },
            'predicted_quantity': round(predicted_quantity, 2)
        }
        
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )

@app.post("/predict/run-forecast", status_code=status.HTTP_200_OK)
def run_forecast_endpoint():
    try:
        results = run_daily_forecasting_logic()
        return {
            "status": "success",
            "message": "Daily forecasting process executed successfully.",
            "details": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Forecasting pipeline execution failed: {str(e)}"
        )

# ==========================================
# 6. AWS LAMBDA ENTRYPOINT HANDLER
# ==========================================
mangum_handler = Mangum(app)

def handler(event, context):
    # Kiểm tra xem có phải cuộc gọi định kỳ từ EventBridge Scheduler không
    if isinstance(event, dict) and (event.get("source") == "aws.events" or "Scheduled Event" in event.get("detail-type", "")):
        logger.info("EventBridge Cron trigger detected. Running daily forecasting logic...")
        try:
            results = run_daily_forecasting_logic()
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "status": "success",
                    "message": "Daily forecast executed by EventBridge schedule.",
                    "details": results
                })
            }
        except Exception as err:
            logger.error("EventBridge execution failed", exc_info=True)
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "status": "error",
                    "message": f"Execution failed: {str(err)}"
                })
            }
            
    # Ngược lại, chuyển tiếp yêu cầu đến Mangum xử lý API Gateway HTTP request
    return mangum_handler(event, context)

# Trigger the cold start download at the very end of module definition
download_and_load_models()
