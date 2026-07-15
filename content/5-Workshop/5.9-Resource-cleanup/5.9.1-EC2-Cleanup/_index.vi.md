---
title: "Xóa các máy chủ EC2"
date: 2024-07-07
weight: 1
chapter: false
pre : " <b> 5.9.1. </b> "
---

### 5.9.1. Dọn dẹp máy chủ ảo Amazon EC2

Để tránh phát sinh chi phí từ việc duy trì các máy chủ ảo và ổ đĩa lưu trữ EBS đi kèm, hãy thực hiện dọn dẹp theo các bước sau:

1. Truy cập **Amazon EC2 Console** -> **Instances**.
2. Tìm và tích chọn các máy chủ của dự án:
   * `Web-Application-Server` (Máy chủ Frontend của Kiệt)
   * `fashion-api-server` (Máy chủ RESTful API của Tùng)
   * `ML-Forecast-Server` (Máy chủ huấn luyện ML của Thành)
3. Nhấp vào nút **Instance state** ở phía trên -> Chọn **Terminate instance**.
4. Xác nhận hành động bằng cách nhấn **Terminate** trong hộp thoại cảnh báo.

> [!NOTE]
> * Trạng thái của instance sẽ chuyển sang `Shutting-down` và sau đó là `Terminated`.
> * Các ổ đĩa lưu trữ EBS (Elastic Block Store) mặc định được thiết lập tự động xóa khi máy chủ bị xóa (*Delete on termination*), giúp giải phóng dung lượng lưu trữ hoàn toàn.

