---
title: "Khởi tạo Cơ sở dữ liệu huấn luyện"
date: 2024-07-07
weight: 2
chapter: false
pre: " <b> 5.2.2. </b> "
---

### 5.2.2. Khởi tạo Cơ sở dữ liệu huấn luyện (`training-db`)

Cơ sở dữ liệu chuyên dụng dùng để lưu trữ các bảng đặc trưng (features) phục vụ riêng cho quy trình huấn luyện mô hình được cấu hình độc lập:

* **Engine Version:** PostgreSQL 18.3
* **Instance Class:** `db.t3.micro`
* **DB Instance Identifier:** `training-db`
* **Master Username:** `dbadmin`
* **Allocated Storage:** 20 GiB (GP2 SSD)
* **Database Name:** `fashiondb`
* **VPC:** `vpc-0426acd9a3039dbc2`

---

#### Các bước khởi tạo trên AWS Console
1. Trên bảng điều khiển **Amazon RDS**, nhấp vào **Create database**.
2. Chọn **Standard create** và engine **PostgreSQL**.
3. Lựa chọn phiên bản **PostgreSQL 18.3** (phiên bản mới nhất để tận dụng các cải tiến xử lý dữ liệu lớn).
4. Chọn bản **Free Tier** và cấu hình DB Instance Identifier là `training-db`.
5. Thiết lập Master Username là `dbadmin` và nhập mật khẩu của bạn.
6. Thiết lập VPC giống với database nghiệp vụ để đảm bảo định tuyến thuận tiện trong cùng một vùng mạng.
