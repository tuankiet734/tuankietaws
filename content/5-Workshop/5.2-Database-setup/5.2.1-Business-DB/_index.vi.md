---
title: "Khởi tạo Cơ sở dữ liệu nghiệp vụ"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.2.1. </b> "
---

### 5.2.1. Khởi tạo Cơ sở dữ liệu nghiệp vụ (`fashion-rds`)

Cơ sở dữ liệu trung tâm lưu trữ thông tin đơn hàng, sản phẩm và cửa hàng thực tế được thiết lập trên dịch vụ **Amazon RDS PostgreSQL** với các thông số sau:

* **Engine Version:** PostgreSQL 15.18
* **Instance Class:** `db.t3.micro` (1 vCPU, 1 GiB RAM)
* **DB Instance Identifier:** `fashion-rds`
* **Master Username:** `dbadmin`
* **Allocated Storage:** 20 GiB (GP2 SSD, hỗ trợ co giãn tự động lên đến 1000 GiB)
* **Database Name:** `fashiondb`
* **VPC:** `vpc-0426acd9a3039dbc2` (Default VPC)
* **Subnet Group:** `default-vpc-0426acd9a3039dbc2` bao gồm các Subnet thuộc cả 3 Availability Zones (`ap-southeast-1a`, `ap-southeast-1b`, `ap-southeast-1c`).

---

#### Các bước khởi tạo trên AWS Console
1. Truy cập dịch vụ **RDS** trên AWS Console.
2. Nhấp vào **Create database**.
3. Chọn **Standard create** và chọn engine **PostgreSQL**.
4. Thiết lập phiên bản **PostgreSQL 15.18-R1** hoặc tương đương.
5. Chọn bản **Free Tier** và cấu hình DB Instance Identifier là `fashion-rds`.
6. Cấu hình thông tin tài khoản Master Username là `dbadmin` và nhập mật khẩu của bạn.
7. Chọn default VPC và bật tùy chọn cho phép truy cập công cộng (**Publicly Accessible**).
