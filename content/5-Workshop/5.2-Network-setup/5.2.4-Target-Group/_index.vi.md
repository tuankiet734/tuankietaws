---
title: "Cấu hình Target Group"
date: 2024-07-07
weight: 4
chapter: false
pre: " <b> 5.2.4. </b> "
---

### 5.2.4. Cấu hình Target Group

Cấu hình Target Group để định tuyến các yêu cầu từ bộ cân bằng tải đến nhóm máy chủ EC2 phù hợp.

1. **Bước 1:** Tại mục **Load Balancing** của dịch vụ EC2, chọn **Target groups**. Nhấn nút **Create target group**:
   * **Target type:** Chọn `Instances`.
   * **Target group name:** Nhập `Internal-Backend-TG`.
   * **Protocol:** `HTTP`, **Port:** `80`.
   * Nhấn **Next** để tiến tới bước tiếp theo.
   
   ![Create Target Group](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232007.png)
2. **Bước 2:** Đăng ký các máy chủ (Targets) vào nhóm:
   * Chọn các máy chủ EC2 mong muốn trong danh sách (ví dụ: `my web sever` với ID `i-0158bbf025496e997`).
   * Nhập cổng dịch vụ nhận luồng dữ liệu (**Port:** `80`) và nhấn nút **Include as pending below**.
   * Xem lại danh sách tại mục **Review targets** và nhấn **Create target group**.
   
   ![Register Targets](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232022.png)
