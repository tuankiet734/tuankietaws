---
title: "Tạo CloudFront Distribution"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.2.1. </b> "
---

### 5.2.1. Tạo CloudFront Distribution

Trong phần này, chúng ta sẽ tạo một CloudFront Distribution để phân phối nội dung từ API Gateway một cách tối ưu và bảo mật.

1. **Bước 1:** Truy cập vào AWS Management Console, tại thanh tìm kiếm nhập "cloudfront" và chọn dịch vụ **CloudFront**.
   
   ![CloudFront Search](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20230833.png)
2. **Bước 2:** Tại giao diện CloudFront Distributions, nhấn nút **Create distribution**. Trong phần **Step 1: Choose a plan**, chọn gói Free ($0/month) và nhấn **Next**.
   
   ![Choose Plan](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20230959.png)
3. **Bước 3:** Tại **Step 2: Get started**, cấu hình các thông số sau:
   * **Distribution name:** Nhập `WebApp-Distribution`.
   * **Distribution type:** Chọn `Single website or app`.
   * Nhấn **Next** để tiếp tục.
   
   ![Get Started](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231043.png)
4. **Bước 4:** Tại **Step 3: Specify origin**, cấu hình thông tin API Gateway làm nguồn cấp dữ liệu (Origin):
   * **Origin type:** Chọn `API Gateway`.
   * **API Gateway origin:** Nhập địa chỉ endpoint API của bạn (ví dụ: `5e0wzdirtc.execute-api.ap-southeast-1.amazonaws.com`).
   * Nhấn **Next** để tiếp tục.
   
   ![Specify Origin](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231122.png)
5. **Bước 5:** Tại **Step 4: Enable security**, bật tính năng Web Application Firewall (WAF) để bảo vệ ứng dụng khỏi các cuộc tấn công phổ biến:
   * Lựa chọn các chế độ bảo vệ mặc định hoặc Rate limiting để chống tấn công từ chối dịch vụ (DDoS).
   * Nhấn **Next**.
   
   ![Enable Security](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231241.png)
6. **Bước 6:** Tại **Step 5: Review and create**, xem lại toàn bộ cấu hình đã thiết lập (Origin, Cache settings, Security) và nhấn nút **Create distribution**.
   
   ![Review and Create](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231320.png)
7. **Bước 7:** Sau khi hoàn tất, hệ thống sẽ chuyển hướng về trang danh sách Distributions. Chờ cho đến khi cột **Status** hiển thị trạng thái **Enabled**.
   
   ![CloudFront Status Enabled](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231521.png)
