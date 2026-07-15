---
title: "Xóa AWS Glue & Lambda"
date: 2024-07-07
weight: 4
chapter: false
pre : " <b> 5.9.4. </b> "
---

### 5.9.4. Xóa các tác vụ Glue Jobs, Lambda Functions và ECR Repositories

Bước cuối cùng là dọn dẹp các dịch vụ serverless tính toán và điều phối lịch trình:

1. **AWS Glue:**
   * Mở trang quản lý **AWS Glue Studio** -> **ETL jobs**. Chọn và xóa các job `de-fashion-rds-extract` và `glue_feature_engineering.py`.
   * Mở phần **Connections** trong AWS Glue, chọn và xóa các Connection kết nối tới các RDS PostgreSQL database.
2. **AWS Lambda:**
   * Mở trang **AWS Lambda Console** -> **Functions**.
   * Chọn hàm Lambda `FashionDemandForecastAPI` (và hàm `DailyForecastTrigger` nếu có), click **Actions** -> Chọn **Delete**.
3. **Amazon ECR:**
   * Mở trang **Amazon ECR Console** -> **Repositories**.
   * Chọn repository `fashion-demand-predictor`, nhấp **Delete** và nhập `delete` để xác nhận xóa hoàn toàn Docker image (tránh phát sinh chi phí lưu trữ tệp image lớn).
4. **Amazon EventBridge Scheduler:**
   * Mở trang **Amazon EventBridge Console** -> **Schedules** (hoặc **Rules**).
   * Chọn daily schedule rule của dự án (ví dụ: `DailyForecastTriggerSchedule`), nhấp **Delete** để hủy lập lịch tự động.

---

{{% notice warning %}}
⚠️ **Cảnh báo dữ liệu:** Sau khi thực hiện xóa cơ sở dữ liệu RDS, các S3 Buckets, ECR Repositories và Lambda, toàn bộ dữ liệu giao dịch lịch sử, đặc trưng và tệp mô hình máy học đóng gói sẽ bị **xóa vĩnh viễn** và không thể phục hồi. Hãy chắc chắn bạn đã lưu trữ hoặc báo cáo tất cả các thông tin chỉ số cần thiết trước khi thực hiện dọn dẹp.
{{% /notice %}}

