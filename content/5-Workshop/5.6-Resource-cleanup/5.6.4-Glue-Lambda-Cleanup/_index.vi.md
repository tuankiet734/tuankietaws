---
title: "Xóa AWS Glue & Lambda"
date: 2024-07-07
weight: 4
chapter: false
pre: " <b> 5.6.4. </b> "
---

### 5.6.4. Xóa các tác vụ Glue Jobs và Lambda Functions

1. Mở trang quản lý **AWS Glue Studio** -> **ETL jobs**, chọn và xóa hai job `de-fashion-rds-extract` và `glue_feature_engineering.py`.
2. Mở trang **AWS Lambda Console** và xóa hàm Lambda cung cấp Model API.
3. Mở trang **Amazon EventBridge** -> **Rules** và xóa quy tắc lập lịch tự động hàng ngày (Daily Schedule Rule).

---

{{% notice warning %}}
⚠️ **Cảnh báo dữ liệu:** Sau khi thực hiện xóa cơ sở dữ liệu RDS và các S3 Buckets, toàn bộ dữ liệu lịch sử giao dịch và các file mô hình sẽ bị **xóa vĩnh viễn** và không thể khôi phục. Hãy chắc chắn bạn đã ghi lại đầy đủ thông tin số liệu cần thiết trước khi thực hiện các bước trên.
{{% /notice %}}
