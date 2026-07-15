---
title: "Tạo Application Load Balancer (ALB)"
date: 2024-07-07
weight: 2
chapter: false
pre: " <b> 5.2.2. </b> "
---

### 5.2.2. Tạo Application Load Balancer (ALB)

Chúng ta tiến hành cấu hình hai bộ cân bằng tải Application Load Balancer: một External ALB tiếp nhận lưu lượng từ internet và một Internal ALB điều phối lưu lượng nội bộ.

#### 1. Cấu hình External Application Load Balancer

1. **Bước 1:** Truy cập vào dịch vụ **EC2**, tại danh mục bên trái tìm đến mục **Load Balancing** và chọn **Load balancers**. Nhấn nút **Create load balancer**, sau đó tại mục **Application Load Balancer** nhấn nút **Create**.
   
   ![Create ALB](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231553.png)
2. **Bước 2:** Cấu hình **Basic configuration** cho External-ALB:
   * **Load balancer name:** Nhập `External-ALB`.
   * **Scheme:** Chọn `Internet-facing` để nhận lưu lượng trực tiếp từ Internet.
   * **IP address type:** Chọn `IPv4`.
   
   ![External ALB Basic Config](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231724.png)
3. **Bước 3:** Tại mục **Network mapping**, liên kết Load Balancer với các vùng sẵn sàng (Availability Zones - AZs) trong VPC:
   * **VPC:** Chọn VPC mặc định của hệ thống.
   * **Mappings:** Tích chọn ít nhất hai AZs là `us-east-1a` và `us-east-1b` cùng các subnet tương ứng để đảm bảo tính sẵn sàng cao.
   
   ![External ALB Network Mapping](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231752.png)
4. **Bước 4:** Tạo Security Group cho Web Server (Nhấn nút "Create security group" để mở tab mới cấu hình):
   * **Security group name:** Nhập `my web`.
   * **Description:** Nhập `Allows SSH access to developers`.
   * **VPC:** Chọn VPC đang cấu hình hệ thống.
   * **Outbound rules:** Chọn Type là `HTTP`, Port range là `80`, Destination là `Anywhere-IPv4` (`0.0.0.0/0`).
   * Nhấn **Create security group** để hoàn tất.
   
   ![Create Security Group](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231809.png)
5. **Bước 5:** Quay lại giao diện tạo ALB, chọn Security groups vừa tạo (`my web`, `default`, `web-alb-sg`, `Web-Template`). Tại mục **Listeners and routing**:
   * **Protocol:** `HTTP`
   * **Port:** `80`
   * **Default action:** Chọn `Forward to target groups` và tạm thời để trống mục Target Group.
   
   ![External ALB Listeners and Security Groups](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231834.png)

#### 2. Cấu hình Internal Application Load Balancer

1. **Bước 1:** Nhấn **Create load balancer** một lần nữa và chọn **Application Load Balancer**. Tại **Basic configuration**:
   * **Load balancer name:** Nhập `Internal-ALB`.
   * **Scheme:** Chọn `Internal` (sử dụng nội bộ trong VPC).
   
   ![Internal ALB Basic Config](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231850.png)
2. **Bước 2:** Tại **Network mapping**, chọn cùng một VPC và các Availability Zones (`us-east-1a`, `us-east-1b`) tương tự bước cấu hình External ALB.
   
   ![Internal ALB Network Mapping](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231906.png)
3. **Bước 3:** Tại **Security groups**, chọn `default` và gán cấu hình Listener cổng `HTTP:80` chuyển tiếp (`Forward`) đến Target Group nội bộ tương ứng.
   
   ![Internal ALB Listeners and Routing](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231923.png)
