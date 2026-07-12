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
2. [Thiết lập cơ sở dữ liệu](5.2-Database-setup/)
3. [Trích xuất đặc trưng với AWS Glue](5.3-Feature-extraction/)
4. [Huấn luyện & Lưu trữ mô hình](5.4-Model-training/)
5. [API dự báo & Lập lịch tự động](5.5-Model-api/)
6. [Dọn dẹp tài nguyên](5.6-Resource-cleanup/)
7. [Video Demo ứng dụng](5.7-Demo/)