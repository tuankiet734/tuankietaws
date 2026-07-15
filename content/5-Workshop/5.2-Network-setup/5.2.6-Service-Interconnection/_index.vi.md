---
title: "Thiết lập kết nối liên thông các dịch vụ"
date: 2024-07-07
weight: 6
chapter: false
pre: " <b> 5.2.6. </b> "
---

### 5.2.6. Thiết lập kết nối liên thông các dịch vụ

Sau khi đã khởi tạo và cấu hình thành công các dịch vụ riêng lẻ, chúng ta cần liên kết chúng lại với nhau để tạo thành một hệ thống hoạt động đồng bộ từ đầu tới cuối:

* **Liên kết CloudFront với API Gateway:** Đảm bảo CloudFront Distribution của bạn nhận API Gateway làm Origin để phân phối nội dung tĩnh và động một cách tối ưu thông qua bộ nhớ đệm (Cache).
* **Cấu hình chuyển tiếp từ Load Balancer:** Kiểm tra lại `External-ALB` và `Internal-ALB` để chắc chắn rằng Default action của Listener cổng `80` được thiết lập là `Forward` đến đúng Target Group tương ứng.
* **Cấu hình bảo mật nâng cao cho các Web Server:** Trên Security Group của các máy chủ EC2 thuộc Auto Scaling Group, chỉ mở cổng HTTP (`80`) cho nguồn (Source) là Security Group của Load Balancer thay vì mở rộng cho toàn bộ Internet. Điều này đảm bảo tính an toàn tối đa cho hệ thống mạng.
