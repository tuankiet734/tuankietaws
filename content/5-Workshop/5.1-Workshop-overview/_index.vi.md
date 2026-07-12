---
title : "Tổng quan kiến trúc"
date : 2024-07-07
weight : 1
chapter : false
pre : " <b> 5.1. </b> "
---

#### Sơ đồ kiến trúc hệ thống

Dưới đây là mô hình kiến trúc hạ tầng mạng và pipeline học máy (machine learning pipeline) được xây dựng trên nền tảng điện toán đám mây **Amazon Web Services (AWS)**:

![overview](/images/5-Workshop/5.1-Workshop-overview/diagram1.png)

#### Thành phần hệ thống

Hệ thống được chia làm hai khu vực chính: **Web Application & APIs** phục vụ người dùng và **Machine Learning Pipeline** chịu trách nhiệm xử lý dữ liệu, huấn luyện mô hình dự báo.

##### 1. Nhóm ứng dụng Web & API (User Access Layer)
* **AWS CloudFront:** Đóng vai trò mạng phân phối nội dung (CDN), tối ưu hóa lưu lượng tải trang bằng cách lưu bộ nhớ đệm (caching) các tài nguyên tĩnh như CSS, JS, hình ảnh sản phẩm.
* **External Application Load Balancer (ALB):** Tiếp nhận yêu cầu HTTP/HTTPS trực tiếp từ người dùng và phân phối tải đến nhóm máy chủ giao diện Web.
* **Web Application (Auto Scaling Group):** Chứa các EC2 instance chạy giao diện web bán lẻ thời trang (như máy chủ `Web-Application-Server`), tự động co giãn dựa trên lượng truy cập thực tế.
* **Internal ALB:** Nhận các yêu cầu gọi API từ lớp giao diện Web chuyển tiếp và điều hướng an toàn vào lớp API nghiệp vụ trong mạng con riêng tư (Private Subnet).
* **RESTful API (Auto Scaling Group):** Chứa các EC2 instance chạy API logic (như máy chủ `fashion-api-server`), quản lý giỏ hàng, đặt hàng, xử lý thanh toán và thông tin khách hàng.

##### 2. Nhóm dữ liệu & Học máy (Data & Machine Learning Pipeline)
* **Central Database (`fashion-rds`):** Hệ quản trị cơ sở dữ liệu quan hệ Amazon RDS PostgreSQL lưu trữ dữ liệu nghiệp vụ chính (giao dịch, sản phẩm, người dùng).
* **Feature Extraction (AWS Glue):** Dịch vụ tính toán phi máy chủ (Serverless Spark) thực hiện ETL trích xuất dữ liệu thô từ `fashion-rds`, thực hiện xử lý dữ liệu và kỹ nghệ đặc trưng thông qua 2 Glue Jobs: `de-fashion-rds-extract` và `glue_feature_engineering.py`.
* **Training Database (`training-db`):** Lưu trữ các đặc trưng (features) đã được trích xuất sẵn sàng cho quá trình huấn luyện mô hình.
* **Training Model (ML-Forecast-Server):** Máy chủ EC2 chuyên dụng (`ML-Forecast-Server`) chịu trách nhiệm kéo dữ liệu đặc trưng từ `training-db`, chạy giải thuật học máy để tạo mô hình dự báo doanh số.
* **Model Storage (Amazon S3):** Lưu trữ tập tin mô hình đã được huấn luyện thành công (`fashion-retail-model-storage`).
* **Model API (AWS Lambda):** Hàm phi máy chủ thực hiện việc tải mô hình từ S3 và cung cấp API dự báo thời gian thực phục vụ cho ứng dụng web.
* **Daily Schedule (Amazon EventBridge):** Bộ lập lịch tự động kích hoạt tiến trình huấn luyện mô hình và trích xuất dữ liệu định kỳ mỗi ngày.
