---
title: "Triển khai Forecast API"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.5.1. </b> "
---

### 5.5.1. Triển khai Forecast API trên AWS Lambda

Chúng ta lựa chọn giải pháp kiến trúc Serverless bằng cách sử dụng **AWS Lambda** để chạy hàm xử lý dự báo thời gian thực (Inference Endpoint). Hàm Lambda sẽ tự động tải file mô hình `.pkl` từ S3 bucket và tính toán kết quả khi có truy vấn gửi tới.

##### Mã nguồn Python của AWS Lambda Handler:
```python
import json
import boto3
import pickle
import os
import pandas as pd

# Khởi tạo S3 client kết nối dịch vụ
s3 = boto3.client('s3')
BUCKET_NAME = "fashion-retail-model-storage"
MODEL_KEY = "models/sales_forecast_model_v1.pkl"
LOCAL_MODEL_PATH = "/tmp/sales_forecast_model_v1.pkl"

# Load model vào bộ nhớ cache ngoài hàm handler để tối ưu Cold Start
model = None

def load_model():
    global model
    if model is None:
        # Tải tệp mô hình từ S3 về thư mục /tmp tạm thời của Lambda Container
        s3.download_file(BUCKET_NAME, MODEL_KEY, LOCAL_MODEL_PATH)
        # Khôi phục đối tượng model qua thư viện pickle
        with open(LOCAL_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    return model

def lambda_handler(event, context):
    try:
        # Load mô hình XGBoost
        predictor = load_model()
        
        # Đọc dữ liệu đầu vào (Features) truyền từ API Gateway dạng JSON
        body = json.loads(event.get('body', '{}'))
        input_data = body.get('features') # Chứa mảng dữ liệu dạng dict/list
        
        # Chuyển đổi dữ liệu sang Pandas DataFrame để đưa vào mô hình dự báo
        df_input = pd.DataFrame(input_data)
        
        # Dự báo kết quả
        predictions = predictor.predict(df_input)
        
        # Trả về kết quả dự báo dưới dạng JSON phản hồi HTTP 200
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # Cho phép gọi từ frontend khác tên miền
            },
            'body': json.dumps({
                'status': 'success',
                'predictions': predictions.tolist()
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

##### Hướng dẫn chụp ảnh minh chứng:
* Truy cập **AWS Lambda Console** -> Chọn hàm Lambda Model API của bạn. Chụp màn hình sơ đồ Designer hoặc mã nguồn. 
* Lưu ảnh vào: `static/images/5-Workshop/5.5-Model-api/lambda-api.png` và bỏ comment dòng dưới đây.

<!-- ![Lambda API](/images/5-Workshop/5.5-Model-api/lambda-api.png) -->
