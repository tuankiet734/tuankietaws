---
title: "Cấu hình Auto Scaling Group (ASG)"
date: 2024-07-07
weight: 5
chapter: false
pre: " <b> 5.2.5. </b> "
---

### 5.2.5. Cấu hình Auto Scaling Group (ASG)

Cấu hình Auto Scaling Group để tự động co giãn số lượng Web Server dựa theo nhu cầu tải thực tế.

1. **Bước 1:** Tại dịch vụ EC2, chọn **Auto Scaling groups** và nhấn **Create Auto Scaling group**:
   * **Auto Scaling group name:** Nhập `WebApp-ASG`.
   * **Launch template:** Chọn mẫu cấu hình khởi chạy thích hợp đã được thiết lập sẵn của bạn.
   * Nhấn **Next**.
   
   ![Create ASG](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232039.png)
2. **Bước 2:** Tại **Step 2: Choose instance launch options**, cấu hình tài nguyên tối thiểu và tối đa cho các máy chủ tự động tăng trưởng:
   * Chọn thuộc tính vCPUs từ 1 đến 5 và dung lượng RAM (Memory) từ 1 đến 5 GiB.
   
   ![ASG Launch Options](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232110.png)
3. **Bước 3:** Chọn VPC và cấu hình vùng mạng cho Auto Scaling Group:
   * **Availability Zones and subnets:** Chọn ít nhất hai vùng `us-east-1a` và `us-east-1b`.
   * **Availability Zone distribution:** Chọn `Balanced best effort`.
   * Nhấn **Next**.
   
   ![ASG Network Mappings](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232127.png)
4. **Bước 4:** Tại **Step 3: Integrate with other services**, liên kết nhóm Auto Scaling với Load Balancer:
   * **Load balancing:** Chọn `Attach to an existing load balancer`.
   * Chọn mục `Choose from your load balancer target groups`.
   * **Existing load balancer target groups:** Chọn Target Group đã tạo ở bước 4 (ví dụ: `Internal-Backend-TG`).
   * Nhấn **Next**.
   
   ![ASG ALB Integration](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232157.png)
5. **Bước 5:** Tại **Step 4: Configure group size and scaling**, cấu hình giới hạn số lượng máy chủ:
   * **Desired capacity:** Nhập `1`.
   * **Min desired capacity:** Nhập `1`.
   * **Max desired capacity:** Nhập `5`.
   * **Automatic scaling:** Chọn `No scaling policies`.
   * Nhấn **Next**.
   
   ![ASG Group Size and Scaling](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232212.png)
6. **Bước 6:** Tại **Step 5: Add notifications**, nhấn **Next** để bỏ qua phần cấu hình gửi thông báo qua SNS (hoặc thiết lập nếu bạn muốn nhận cảnh báo khi hệ thống thay đổi quy mô).
   
   ![ASG Notifications](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232230.png)
7. **Bước 7:** Tại **Step 7: Review**, kiểm tra kỹ lưỡng các cài đặt cấu hình nhóm Auto Scaling Group của bạn và nhấn nút **Create Auto Scaling group** để chính thức kích hoạt.
   
   ![ASG Review and Create](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232245.png)
