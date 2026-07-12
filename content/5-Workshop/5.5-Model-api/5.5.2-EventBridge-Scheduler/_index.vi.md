---
title: "Tự động hóa Pipeline"
date: 2024-07-07
weight: 2
chapter: false
pre: " <b> 5.5.2. </b> "
---

### 5.5.2. Tự động hóa Pipeline với Amazon EventBridge

Để đảm bảo mô hình luôn dự báo chính xác dựa trên lượng dữ liệu giao dịch bán hàng thay đổi hàng ngày, toàn bộ Pipeline cần được tự động hóa quy trình chạy theo lịch trình biểu thức Cron.

##### Cơ chế hoạt động của Scheduler Rule:
1. Quy tắc **Amazon EventBridge Rule** được thiết lập kích hoạt theo thời gian định sẵn (Ví dụ: `cron(0 0 * * ? *)` - Chạy vào lúc 00:00 hàng ngày).
2. Khi EventBridge kích hoạt, nó sẽ gửi tín hiệu khởi chạy tác vụ AWS Glue Job trích xuất đầu tiên `de-fashion-rds-extract`.
3. Sau khi job này kết thúc thành công, Glue Trigger sẽ nối tiếp kích hoạt job Spark `glue_feature_engineering.py` chạy xử lý đặc trưng.
4. Một thông báo Amazon SNS (Simple Notification Service) được gửi đến máy chủ `ML-Forecast-Server` để gọi script Python chạy lại tiến trình huấn luyện mô hình và cập nhật file `.pkl` mới lên S3.

##### Hướng dẫn chụp ảnh minh chứng:
* Truy cập **Amazon EventBridge Console** -> **Rules**. Tìm kiếm rule daily schedule của bạn và chụp màn hình trang thông tin chi tiết. 
* Lưu ảnh vào: `static/images/5-Workshop/5.5-Model-api/eventbridge-schedule.png` và bỏ comment dòng dưới đây.

<!-- ![EventBridge Rule](/images/5-Workshop/5.5-Model-api/eventbridge-schedule.png) -->
