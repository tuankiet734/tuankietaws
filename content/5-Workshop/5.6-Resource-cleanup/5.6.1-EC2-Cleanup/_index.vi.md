---
title: "Xóa các máy chủ EC2"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.6.1. </b> "
---

### 5.6.1. Dọn dẹp máy chủ ảo Amazon EC2

1. Truy cập **Amazon EC2 Console** -> **Instances**.
2. Tìm và chọn các máy chủ: `Web-Application-Server`, `fashion-api-server`, và `ML-Forecast-Server` (hoặc các Auto Scaling Groups tương ứng).
3. Nhấp vào nút **Instance state** -> Chọn **Terminate instance** để xóa bỏ hoàn toàn máy chủ và giải phóng các phân vùng ổ đĩa EBS đi kèm.
