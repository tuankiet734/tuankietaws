---
title: "S3 Model Storage"
date: 2024-07-07
weight: 3
chapter: false
pre: " <b> 5.4.3. </b> "
---

### 5.4.3. Staging and Uploading Model Artifacts to S3

Once the `sales_forecast_model_v1.pkl` file is saved locally on the EC2 server, the pipeline executes a script utilizing the AWS SDK for Python (`boto3`) to upload it to Amazon S3.

##### S3 Upload Script:
```python
# Initialize S3 client connection
s3_client = boto3.client('s3', region_name='ap-southeast-1')
bucket_name = "fashion-retail-model-storage"
s3_key = "models/sales_forecast_model_v1.pkl"

# Upload model file to bucket
s3_client.upload_file(model_filename, bucket_name, s3_key)
print(f"Model saved to S3: s3://{bucket_name}/{s3_key}")
```

##### Screenshot Guide:
* Open the **Amazon S3 Console** -> Bucket `fashion-retail-model-storage`. Take a screenshot showing your uploaded `.pkl` model file inside the folder structure.
* Save the screenshot in: `static/images/5-Workshop/5.4-Model-training/s3-models.png` and remove the comment markdown tags.

<!-- ![S3 Models](/images/5-Workshop/5.4-Model-training/s3-models.png) -->
