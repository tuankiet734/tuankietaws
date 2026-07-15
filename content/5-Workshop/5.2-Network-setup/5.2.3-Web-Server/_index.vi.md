---
title: "Khởi tạo EC2 Instance (Web Server)"
date: 2024-07-07
weight: 3
chapter: false
pre: " <b> 5.2.3. </b> "
---

### 5.2.3. Khởi tạo EC2 Instance (Web Server)

Tiến hành khởi tạo một máy chủ ảo EC2 để đóng vai trò làm Web Application Server chạy ứng dụng retail storefront.

1. **Bước 1:** Truy cập dịch vụ **EC2**, tại mục **Instances** nhấn nút **Launch an instance** để khởi tạo một máy chủ ảo Web Server mới:
   * **Name and tags:** Nhập `Web-Application-Server`.
   * **OS Image (AMI):** Chọn `Ubuntu`, phiên bản `Ubuntu Server 26.04 LTS (HVM)`, SSD Volume Type.
   
   ![Launch EC2 Instance](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231937.png)
2. **Bước 2:** Cấu hình khóa bảo mật và mạng cho máy chủ:
   * **Key pair:** Chọn Key pair của bạn để kết nối bảo mật.
   * **VPC:** Chọn VPC của hệ thống.
   * **Auto-assign public IP:** Chọn `Enable`.
   * **Firewall (security groups):** Tích chọn `Allow SSH traffic`, `Allow HTTPS traffic`, và `Allow HTTP traffic` để cho phép các lưu lượng mạng cần thiết.
   
   ![EC2 Key Pair and Network Settings](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231953.png)
3. **Bước 3:** Nhấn **Launch instance** để hoàn tất quá trình tạo máy chủ ảo.
