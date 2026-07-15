---
title: "Model Serialization & Storage"
date: 2024-07-07
weight: 3
chapter: false
pre : " <b> 5.5.3. </b> "
---

### 5.5.3. Serializing and Uploading Models to Amazon S3

After the training script runs successfully on our EC2 server, the model and preprocessing elements are serialized into 3 separate binary pickle files using the `joblib` library to minimize memory overhead:

1. **`lightgbm_demand_model.pkl`**: Contains the decision tree structures and trained weights of the LightGBM Regressor.
2. **`standard_scaler.pkl`**: Stores the computed feature means and standard deviations of the numerical features for validation data scaling.
3. **`label_encoders.pkl`**: A lookup dictionary containing fit `LabelEncoder` objects for all categorical fields (sku, size, color, category, etc.).

These artifacts are securely pushed to **Amazon S3** using the AWS SDK `boto3`.

##### Model Upload Script Snippet:
```python
import boto3

s3_client = boto3.client('s3', region_name='ap-southeast-1')
bucket_name = "fashion-retail-model-storage"
files = ["lightgbm_demand_model.pkl", "standard_scaler.pkl", "label_encoders.pkl"]

for file in files:
    s3_key = f"models/{file}"
    s3_client.upload_file(file, bucket_name, s3_key)
    print(f"Uploaded: s3://{bucket_name}/{s3_key}")
```

---

#### Verification on Amazon S3:

![S3 Models](/images/5-Workshop/5.5-Model-training/s3-models.png)
