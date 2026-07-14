---
title: "Minh chứng hoạt động"
date: 2024-07-07
weight: 4
chapter: false
pre: " <b> 5.3.4. </b> "
---

### 5.3.4. Minh chứng hoạt động trên AWS Console

Để minh chứng các Glue Jobs chạy thành công và ghi nhận các logs liên quan:

#### Các bước thực hiện:
1. Mở trang quản trị dịch vụ **AWS Glue Studio**.
2. Chọn **ETL jobs** và nhấp vào danh sách để kiểm tra các run lịch sử của `de-fashion-rds-extract` và `glue_feature_engineering.py`.
3. Kiểm tra cột **Run status** hiển thị trạng thái **Succeeded** (Thành công).
4. Nhấp vào **Run details** và chọn xem log trên **Amazon CloudWatch Logs** để thấy thông tin in ra:
   * Đối với job extract: `Extract thanh cong!`
   * Đối với job feature: In ra báo cáo chất lượng `[FEATURES] TAT CA FEATURES HOP LE - OK!` và `Tong records: ...`

##### Hướng dẫn chụp ảnh minh chứng:
* Chụp màn hình danh sách jobs hiển thị cả 2 tác vụ trên và lưu vào thư mục dự án của bạn theo đường dẫn: `static/AWS/images/5-Workshop/5.3-Feature-extraction/glue-jobs.png` và xóa comment dòng dưới đây.

![Glue Jobs](/AWS/images/5-Workshop/5.3-Feature-extraction/glue-jobs.png)
