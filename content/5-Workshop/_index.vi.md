---
title: "Workshop"
date: 2024-07-07
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Xây dựng Ứng dụng Web Thời trang & Pipeline Machine Learning Dự báo Doanh số

#### Tổng quan

Trong bài thực hành (workshop) này, chúng ta sẽ xây dựng một kiến trúc ứng dụng web bán lẻ thời trang hoàn chỉnh trên **AWS Cloud**, kết hợp với một pipeline tự động hóa quy trình trích xuất dữ liệu, kỹ nghệ đặc trưng (feature engineering) và huấn luyện mô hình dự báo doanh số (ML forecasting pipeline).

Hệ thống được thiết kế nhằm giải quyết bài toán tối ưu hóa hàng tồn kho bằng cách dự báo nhu cầu mua sắm của khách hàng dựa trên dữ liệu lịch sử giao dịch. Chúng ta sẽ làm quen với việc triển khai các thành phần hạ tầng mạng, cân bằng tải, cơ sở dữ liệu và các dịch vụ tính toán dữ liệu lớn chuyên sâu như **AWS Glue**, **Amazon EC2**, **Amazon S3** và **AWS Lambda**.

#### Nội dung

1. [Tổng quan kiến trúc](5.1-Workshop-overview/)
2. [Cấu hình hệ thống mạng](5.2-Network-setup/)
3. [Thiết lập cơ sở dữ liệu](5.3-Database-setup/)
4. [Trích xuất đặc trưng với AWS Glue](5.4-Feature-extraction/)
5. [Huấn luyện & Lưu trữ mô hình](5.5-Model-training/)
6. [API dự báo & Lập lịch tự động](5.6-Model-api/)
7. [Giao diện Cổng thông tin & Phân quyền](5.7-Web-Portal/)
8. [Triển khai Web App lên EC2](5.8-EC2-Deployment/)
9. [Dọn dẹp tài nguyên](5.9-Resource-cleanup/)
10. [Video Demo ứng dụng](5.10-Demo/)