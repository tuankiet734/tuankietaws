---
title: "Đóng gói và lưu trữ mô hình"
date: 2024-07-07
weight: 3
chapter: false
pre: " <b> 5.4.3. </b> "
---

### 5.4.3. Đóng gói và Lưu trữ mô hình lên S3

Sau khi file mô hình `sales_forecast_model_v1.pkl` được xuất thành công trên máy chủ EC2, nó sẽ được tự động tải lên lưu trữ an toàn tại **Amazon S3** thông qua thư viện AWS SDK `boto3`.

##### Đoạn code tải mô hình lên S3:
```python
# Khởi tạo s3 client kết nối dịch vụ
s3_client = boto3.client('s3', region_name='ap-southeast-1')
bucket_name = "fashion-retail-model-storage"
s3_key = "models/sales_forecast_model_v1.pkl"

# Tải file lên bucket của dự án
s3_client.upload_file(model_filename, bucket_name, s3_key)
print(f"Đã lưu mô hình lên S3: s3://{bucket_name}/{s3_key}")
```

##### Hướng dẫn chụp ảnh minh chứng:
* Truy cập dịch vụ **Amazon S3 Console** -> Bucket `fashion-retail-model-storage`. Chụp màn hình danh sách thư mục và file mô hình `.pkl` đã tải lên thành công.
* Lưu ảnh vào: `static/images/5-Workshop/5.4-Model-training/s3-models.png` và xóa dấu comment dòng dưới đây.

<!-- ![S3 Models](/images/5-Workshop/5.4-Model-training/s3-models.png) -->
