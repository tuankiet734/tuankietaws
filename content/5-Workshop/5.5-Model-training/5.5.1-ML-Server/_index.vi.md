---
title: "Khởi tạo Máy chủ Huấn luyện"
date: 2024-07-07
weight: 1
chapter: false
pre : " <b> 5.5.1. </b> "
---

### 5.5.1. Khởi tạo Máy chủ Huấn luyện EC2 (`ML-Forecast-Server`)

Quy trình huấn luyện mô hình học máy yêu cầu một máy chủ tính toán ảo ổn định, do đó chúng ta triển khai một instance chuyên dụng trên **Amazon EC2**:

* **Tên Instance (Name Tag):** `ML-Forecast-Server`
* **Instance ID:** `i-019ac66f1b864b96a`
* **Loại Instance:** `t2.micro`
* **Hệ điều hành:** Ubuntu Linux (64-bit x86)
* **Vị trí mạng:** Chạy trong mạng con công cộng thuộc Availability Zone `ap-southeast-1b` (Singapore).
* **Mạng và Bảo mật (Security Group - `sg-0579af9926812195b` / `launch-wizard-3`):**
  * **Inbound Rules:** Cho phép kết nối SSH (cổng 22) từ địa chỉ IP cá nhân của nhà phát triển để cài đặt cấu hình.
  * **Outbound Rules:** 
    * Cho phép kết nối đến cổng `5432` của cơ sở dữ liệu `training-db` (hoặc `fashion-rds`) để đọc dữ liệu đặc trưng.
    * Cho phép cổng HTTPS (443) ra ngoài Internet để tải các thư viện Python cần thiết (`lightgbm`, `scikit-learn`, `psycopg2-binary`, v.v.).

---

#### Quy trình khởi tạo chi tiết trên AWS Console:

1. **Truy cập dịch vụ:** Đăng nhập vào **AWS Console**, tìm kiếm `EC2` và chọn dịch vụ **EC2**.
2. **Khởi chạy Instance:** Tại trang EC2 Dashboard, chọn **Launch instance**.
3. **Cấu hình Tên & OS:**
   * **Name tag:** Đặt tên là `ML-Forecast-Server`.
   * **OS (AMI):** Chọn **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type** (64-bit x86).
4. **Loại Instance & Khóa (Key Pair):**
   * **Instance type:** Chọn `t2.micro` (hoặc nâng cấp lên `t2.medium` nếu muốn huấn luyện nhanh hơn).
   * **Key pair:** Chọn key pair sẵn có (`Thanh_key.pem` hoặc `EC2.pem`) để kết nối SSH.
5. **Cấu hình Mạng (Network Settings):**
   * **VPC:** Chọn Default VPC.
   * **Subnet:** Chọn public subnet bất kỳ (ví dụ: AZ `ap-southeast-1b`).
   * **Auto-assign public IP:** Chọn **Enable** để có IP công cộng kết nối SSH.
   * **Security group:** Chọn **Create security group**, đặt tên là `ml-server-sg` và thiết lập các rule Inbound/Outbound như trên.
6. **Lưu trữ (Storage):** Cấu hình ổ đĩa **gp3** với dung lượng tối thiểu **15-20 GB** để đủ không gian cài đặt thư viện và lưu tệp mô hình tạm thời.
7. **Khởi chạy:** Nhấp **Launch instance** và đợi máy chủ chuyển sang trạng thái **Running**.

---

#### Minh chứng thực tế trên AWS Console:

![EC2 Server](/images/5-Workshop/5.5-Model-training/ec2-ml-server.png)

