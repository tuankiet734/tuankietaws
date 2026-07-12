---
title: "Forecast API Deployment"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.5.1. </b> "
---

### 5.5.1. Implementing the Forecast API on AWS Lambda

We deploy a serverless inference endpoint using **AWS Lambda**. When called, the Lambda function downloads the serialized `.pkl` model file from S3, parses the request, and calculates real-time predictions.

##### AWS Lambda Handler Python Code:
```python
import json
import boto3
import pickle
import os
import pandas as pd

# Initialize S3 client connection
s3 = boto3.client('s3')
BUCKET_NAME = "fashion-retail-model-storage"
MODEL_KEY = "models/sales_forecast_model_v1.pkl"
LOCAL_MODEL_PATH = "/tmp/sales_forecast_model_v1.pkl"

# Keep the loaded model cached in container memory to minimize cold start latency
model = None

def load_model():
    global model
    if model is None:
        # Download the model artifact from S3 to container tmp storage
        s3.download_file(BUCKET_NAME, MODEL_KEY, LOCAL_MODEL_PATH)
        # Unpickle the model object
        with open(LOCAL_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    return model

def lambda_handler(event, context):
    try:
        # Load XGBoost model
        predictor = load_model()
        
        # Parse features from HTTP request body
        body = json.loads(event.get('body', '{}'))
        input_data = body.get('features') # Expected to be an array of dicts
        
        # Convert input into a Pandas DataFrame
        df_input = pd.DataFrame(input_data)
        
        # Compute forecasts
        predictions = predictor.predict(df_input)
        
        # Return HTTP 200 with forecast arrays
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # Allow requests from all origins
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

##### Screenshot Guide:
* Open **AWS Lambda Console** -> Select your Model API function. Take a screenshot showing the Designer diagram or the code view. 
* Save the screenshot in: `static/images/5-Workshop/5.5-Model-api/lambda-api.png` and remove the comment markdown tags.

<!-- ![Lambda API](/images/5-Workshop/5.5-Model-api/lambda-api.png) -->
