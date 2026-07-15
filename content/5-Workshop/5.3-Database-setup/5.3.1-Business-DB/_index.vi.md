---
title: "Khởi tạo Cơ sở dữ liệu nghiệp vụ"
date: 2024-07-07
weight: 1
chapter: false
pre : " <b> 5.3.1. </b> "
---

### 5.3.1. Khởi tạo Cơ sở dữ liệu nghiệp vụ (`fashion-rds`)

Cơ sở dữ liệu trung tâm lưu trữ thông tin đơn hàng, giao dịch, sản phẩm và cửa hàng được thiết lập trên dịch vụ **Amazon RDS PostgreSQL** với các thông số chi tiết:
* **Database Engine:** PostgreSQL 15.18
* **Instance Class:** `db.t3.micro` (1 vCPU, 1 GiB RAM)
* **DB Instance Identifier:** `fashion-rds`
* **Master Username:** `dbadmin`
* **Allocated Storage:** 20 GiB (GP2 SSD, Auto-scaling enabled)
* **Database Name:** `fashiondb`
* **VPC:** Default VPC (`vpc-0426acd9a3039dbc2`)
* **Endpoint thực tế:** `fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com`

---

#### Hướng dẫn chi tiết các bước khởi tạo trên AWS Console:

1. **Truy cập dịch vụ:** Đăng nhập vào **AWS Management Console**, tại thanh tìm kiếm trên cùng, gõ `RDS` và chọn dịch vụ **RDS**.
2. **Khởi tạo Database:** Trong giao diện RDS Dashboard, nhấp vào nút **Create database** màu cam.
3. **Chọn phương thức khởi tạo:** Chọn **Standard create** để có thể tùy biến cấu hình chi tiết.
4. **Chọn Engine Options:** 
   * Chọn loại Engine là **PostgreSQL**.
   * Tại mục **Engine Version**, nhấp vào menu thả xuống và chọn phiên bản **PostgreSQL 15.18-R1** hoặc phiên bản tương đương.
5. **Chọn Template:** Chọn **Free Tier** để đảm bảo chi phí tối ưu (cấu hình này tự động giới hạn loại instance về `db.t3.micro` và ổ đĩa 20 GiB).
6. **Cấu hình định danh (Settings):**
   * **DB instance identifier:** Nhập `fashion-rds`.
   * **Credentials specification:** 
     * **Master username:** Nhập `dbadmin`.
     * **Master password:** Nhập mật khẩu bảo mật của bạn.
7. **Cấu hình Instance & Storage:** Giữ cấu hình mặc định là `db.t3.micro` và loại lưu trữ **gp2** với **20 GiB** dung lượng. Bật tùy chọn **Enable storage autoscaling**.
8. **Cấu hình Kết nối mạng (Connectivity):**
   * **Virtual Private Cloud (VPC):** Chọn Default VPC.
   * **Public access:** Tích chọn **Yes** (Đảm bảo pgAdmin hoặc DBeaver từ máy cá nhân có thể kết nối thử nghiệm).
   * **VPC security group:** Chọn **Create new**, đặt tên cho Security Group mới để cấu hình mạng.
9. **Cấu hình bổ sung (Additional configuration):** Nhấp mở rộng phần này ở cuối trang:
   * **Initial database name:** Nhập `fashiondb`.
   * Giữ nguyên các cấu hình Backup và Encryption mặc định.
10. **Hoàn tất:** Nhấp vào nút **Create database** ở cuối trang. Hệ thống sẽ mất khoảng 5-7 phút để khởi tạo máy chủ cơ sở dữ liệu.

---

#### Minh chứng thực tế trên AWS Console:

![Central RDS Database](/images/5-Workshop/5.3-Database-setup/rds-all-databases.png)