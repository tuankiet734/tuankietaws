---
title: "Cấu hình Mạng và Bảo mật"
date: 2024-07-07
weight: 3
chapter: false
pre: " <b> 5.2.3. </b> "
---

### 5.2.3. Cấu hình Mạng và Bảo mật (Security & Network Groups)

Cả hai cơ sở dữ liệu đều được thiết lập cấu hình mạng và bảo mật nhằm đảm bảo các dịch vụ trung gian (AWS Glue, EC2, Lambda) có thể kết nối an toàn nhưng vẫn ngăn chặn các truy cập trái phép.

* **Publicly Accessible:** Đặt là `True` để cho phép các client truy vấn từ bên ngoài VPC.
* **Security Group (`sg-0fecd1d2df90f2a69`):**
  * **Inbound Rules:**
    * Cổng `5432` / Protocol TCP: Cho phép truy cập từ địa chỉ IP cá nhân của nhà phát triển (Dành cho pgAdmin/DBeaver).
    * Cổng `5432` / Protocol TCP: Cho phép kết nối từ máy chủ EC2 `ML-Forecast-Server` (`sg-0579af9926812195b`).
    * Cổng `5432` / Protocol TCP: Tự tham chiếu chính nó (Self-referencing rule) cho phép tác vụ AWS Glue kết nối JDBC an toàn.
  * **Outbound Rules:** Cho phép tất cả lưu lượng ra ngoài (Mặc định).
* **Mã hóa lưu trữ (Storage Encryption):** Kích hoạt mã hóa ổ đĩa thông qua khóa quản lý khóa **AWS KMS** mặc định (`fe12be50-a2cf-44d1-a1da-3ce27e40686d`).

##### Hướng dẫn chụp ảnh minh chứng hoạt động:
* Đăng nhập **AWS Management Console** -> **RDS** -> **Databases**. Chụp màn hình danh sách cơ sở dữ liệu của bạn hiển thị cả `fashion-rds` và `training-db` với trạng thái **Available**.
* Lưu hình ảnh vào thư mục dự án của bạn theo đường dẫn: `static/images/5-Workshop/5.2-Database-setup/rds-console.png` và xóa comment dòng dưới trong file.

<!-- ![RDS Console](/images/5-Workshop/5.2-Database-setup/rds-console.png) -->
