---
title: "Minh chứng hoạt động"
date: 2024-07-07
weight: 4
chapter: false
pre : " <b> 5.4.4. </b> "
---

### 5.4.4. Minh chứng hoạt động trích xuất dữ liệu trên AWS Console

Sau khi kích hoạt chạy thử nghiệm các Glue Jobs, chúng ta có thể kiểm tra danh sách chạy và xác nhận trạng thái thành công.

---

#### Các bước kiểm tra chạy thành công:

1. **Mở AWS Glue Studio:** Nhấp vào **ETL jobs** ở menu trái.
2. **Chọn Job chạy:** Nhấp chọn job `de-fashion-rds-extract` hoặc `glue_feature_engineering.py`.
3. **Kiểm tra lịch sử chạy (Runs):** Nhấp chọn tab **Runs** ở phần giao diện quản lý của job.
4. **Kiểm tra trạng thái:** Xác nhận cột **Run status** hiển thị biểu tượng tích xanh lá cây kèm chữ **Succeeded** (Thành công).
5. **Xem Log:** Nhấp chọn **Output logs** ở phần thông tin chạy để được chuyển hướng sang CloudWatch Logs xem chi tiết thông điệp kết xuất.

---

#### Minh chứng hoạt động trên AWS Console:

Hình ảnh danh sách chạy và trạng thái của các AWS Glue Jobs được chụp trực tiếp trên AWS Management Console:

![Glue Jobs](/images/5-Workshop/5.4-Feature-extraction/glue-run-succeeded.png)