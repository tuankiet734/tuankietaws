---
title : "Thiết lập cơ sở dữ liệu"
date : 2024-07-07
weight : 3
chapter : false
pre : " <b> 5.3. </b> "
---

Để chuẩn bị lưu trữ dữ liệu cho toàn bộ hệ thống, chúng ta cần triển khai hai cơ sở dữ liệu quan hệ **Amazon RDS PostgreSQL** trên AWS: một cơ sở dữ liệu trung tâm lưu trữ thông tin giao dịch bán hàng trực tiếp (`fashion-rds`) và một cơ sở dữ liệu chuyên dụng để lưu trữ các bảng đặc trưng đã qua xử lý phục vụ huấn luyện mô hình học máy (`training-db`).

---

{{% children /%}}
