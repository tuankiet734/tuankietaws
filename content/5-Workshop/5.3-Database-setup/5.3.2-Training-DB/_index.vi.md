---
title: "Khởi tạo Cơ sở dữ liệu huấn luyện"
date: 2024-07-07
weight : 3
chapter: false
pre : " <b> 5.3.2. </b> "
---

### 5.3.2. Khởi tạo Cơ sở dữ liệu huấn luyện (`training-db`)

Cơ sở dữ liệu huấn luyện chuyên dụng được sử dụng riêng để lưu trữ các bảng đặc trưng (features) đã được trích xuất hoàn chỉnh qua Spark ETL, nhằm phục vụ trực tiếp cho tiến trình máy học:
* **Database Engine:** PostgreSQL 18.3
* **Instance Class:** `db.t3.micro` (1 vCPU, 1 GiB RAM)
* **DB Instance Identifier:** `training-db`
* **Master Username:** `dbadmin`
* **Allocated Storage:** 20 GiB (GP2 SSD)
* **Database Name:** `fashiondb`
* **VPC:** Default VPC (`vpc-0426acd9a3039dbc2`)
* **Endpoint thực tế:** `training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com`

---

#### Hướng dẫn chi tiết các bước khởi tạo trên AWS Console:

1. **Truy cập dịch vụ:** Mở bảng điều khiển **Amazon RDS**, nhấp vào danh sách **Databases** ở menu bên trái.
2. **Khởi tạo Database:** Nhấp vào nút **Create database** màu cam ở phía trên góc phải.
3. **Chọn cấu hình:**
   * Chọn **Standard create** và engine **PostgreSQL**.
   * Tại mục **Engine Version**, lựa chọn phiên bản **PostgreSQL 18.3** (đây là phiên bản mới nhất nhằm tận dụng tối đa các cải tiến và hiệu năng tối ưu của Postgres cho xử lý dữ liệu đặc trưng).
4. **Chọn Template:** Chọn **Free Tier**.
5. **Cài đặt định danh:**
   * **DB instance identifier:** Nhập `training-db`.
   * **Master username:** Nhập `dbadmin`.
   * **Master password:** Nhập mật khẩu quản trị của bạn.
6. **Mạng và Bảo mật (Connectivity):**
   * Chọn Default VPC.
   * **Public access:** Tích chọn **Yes** (Để thuận tiện cho việc kết nối và kiểm tra tính hợp lệ của dữ liệu đặc trưng).
   * **VPC security group:** Chọn **Create new**, đặt tên rõ ràng cho Security Group.
7. **Cấu hình bổ sung (Additional configuration):**
   * **Initial database name:** Nhập `fashiondb`.
8. **Hoàn tất:** Nhấp **Create database** và chờ hệ thống hoàn thành khởi tạo.

---

#### Minh chứng thực tế trên AWS Console:

![Training RDS Database](/images/5-Workshop/5.3-Database-setup/training-db-detail.png)