---
title: "Tổng quan Quy trình ETL"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.3.1. </b> "
---

### 5.3.1. Tổng quan Quy trình ETL trên AWS Glue

Quy trình xử lý dữ liệu phục vụ huấn luyện mô hình dự báo học máy bao gồm hai giai đoạn chính chạy tuần tự:

{{<mermaid>}}
graph TD
    RDS[Central RDS] -->|1. Extract| PythonJob[de-fashion-rds-extract]
    PythonJob -->|Lưu trữ dạng Parquet| S3Landing[S3 Landing Zone]
    S3Landing -->|2. Ingest| SparkJob[glue_feature_engineering.py]
    SparkJob -->|Tính toán Lags, Rolling, Velocity| ProcessedFeatures[Feature Calculations]
    ProcessedFeatures -->|3. Ghi song song| CentralDB[Central RDS]
    ProcessedFeatures -->|3. Ghi song song| TrainingDB[Training RDS]
{{</mermaid>}}

#### Chi tiết các bước thực hiện:
1. **Trích xuất dữ liệu thô (Extract):** Tác vụ python shell kết nối trực tiếp đến cơ sở dữ liệu `fashion-rds` để lấy các bảng giao dịch (`transactions`), sản phẩm (`products`), cửa hàng (`stores`) và lưu tạm thời lên Amazon S3 dưới dạng file Parquet.
2. **Kỹ nghệ đặc trưng (Transform):** Tác vụ Spark phân tán đọc dữ liệu Parquet từ S3, xử lý làm sạch, điền giá trị khuyết (như giá trị trung bình giá bán của từng loại sản phẩm, màu sắc thịnh hành) và sử dụng các biểu thức **Window Functions** trong PySpark để tính toán các chỉ số đặc trưng theo chuỗi thời gian cho từng sản phẩm tại mỗi cửa hàng.
3. **Lưu trữ dữ liệu xử lý (Load):** Ghi dữ liệu đặc trưng đã hoàn thiện xuống cả hai cơ sở dữ liệu để phục vụ kiểm tra và phục vụ trực tiếp cho tiến trình học máy.
