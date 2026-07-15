---
title: "Đóng gói và lưu trữ mô hình"
date: 2024-07-07
weight: 3
chapter: false
pre : " <b> 5.5.3. </b> "
---

### 5.5.3. Đóng gói và Lưu trữ mô hình lên S3

Sau khi kịch bản huấn luyện chạy thành công trên máy chủ EC2, mô hình và các thành phần tiền xử lý được tuần tự hóa (serialize) thành 3 tệp nhị phân độc lập bằng thư viện `joblib` để tối ưu kích thước bộ nhớ:

1. **`lightgbm_demand_model.pkl`**: Chứa tham số mạng và cấu trúc các cây quyết định của mô hình LightGBM Regressor.
2. **`standard_scaler.pkl`**: Chứa giá trị trung bình (mean) và độ lệch chuẩn (std) của các đặc trưng số để thực hiện quy chuẩn hóa dữ liệu đầu vào.
3. **`label_encoders.pkl`**: Từ điển lưu trữ các đối tượng mã hóa nhãn chuỗi sang số nguyên phục vụ cho các cột phân loại (sku, size, color, category, v.v.).

Các tệp này được tự động hóa tải lên **Amazon S3** thông qua thư viện AWS SDK `boto3`.

##### Đoạn mã nguồn tải các file mô hình lên S3:
```python
import boto3

s3_client = boto3.client('s3', region_name='ap-southeast-1')
bucket_name = "fashion-retail-model-storage"
files = ["lightgbm_demand_model.pkl", "standard_scaler.pkl", "label_encoders.pkl"]

for file in files:
    s3_key = f"models/{file}"
    s3_client.upload_file(file, bucket_name, s3_key)
    print(f"Đã lưu mô hình lên S3: s3://{bucket_name}/{s3_key}")
```

---

#### Minh chứng thực tế lưu trữ trên Amazon S3:

![S3 Models](/images/5-Workshop/5.5-Model-training/s3-models.png)

