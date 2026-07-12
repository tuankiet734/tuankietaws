---
title: "Khởi tạo Máy chủ Huấn luyện"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.4.1. </b> "
---

### 5.4.1. Khởi tạo Máy chủ Huấn luyện EC2 (`ML-Forecast-Server`)

Quy trình huấn luyện mô hình học máy yêu cầu một máy chủ tính toán ảo ổn định, do đó chúng ta triển khai một instance chuyên dụng trên **Amazon EC2**:

* **Tên Instance (Name Tag):** `ML-Forecast-Server`
* **Instance ID:** `i-019ac66f1b864b96a`
* **Loại Instance:** `t2.micro`
* **Hệ điều hành:** Ubuntu Linux (64-bit x86)
* **Vị trí mạng:** Chạy trong mạng con công cộng thuộc Availability Zone `ap-southeast-1b` (Singapore).
* **Mạng và Bảo mật (Security Group - `sg-0579af9926812195b` / `launch-wizard-3`):**
  * Cho phép kết nối SSH (cổng 22) từ địa chỉ IP cá nhân của nhà phát triển để cài đặt cấu hình.
  * Cho phép Outbound kết nối đến cổng `5432` của `training-db` để đọc dữ liệu đặc trưng.
  * Cho phép Outbound cổng HTTPS (443) ra ngoài Internet để tải các thư viện Python.

##### Hướng dẫn chụp ảnh minh chứng:
* Truy cập **Amazon EC2 Console** -> **Instances**. Chụp màn hình thông tin chi tiết của máy chủ `ML-Forecast-Server` ở trạng thái **Running**.
* Lưu ảnh vào: `static/images/5-Workshop/5.4-Model-training/ec2-ml-server.png` và xóa dấu comment dòng dưới đây.

<!-- ![EC2 Server](/images/5-Workshop/5.4-Model-training/ec2-ml-server.png) -->
