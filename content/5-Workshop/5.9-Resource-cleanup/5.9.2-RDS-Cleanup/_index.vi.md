---
title: "Xóa các cơ sở dữ liệu RDS"
date: 2024-07-07
weight: 2
chapter: false
pre : " <b> 5.9.2. </b> "
---

### 5.9.2. Xóa các cơ sở dữ liệu quan hệ Amazon RDS

Để giải phóng bộ nhớ lưu trữ cơ sở dữ liệu quan hệ đang chạy liên tục, thực hiện xóa các thực thể RDS như sau:

1. Truy cập **Amazon RDS Console** -> **Databases**.
2. Tìm và chọn các thực thể cơ sở dữ liệu của nhóm:
   * `fashion-rds` (Cơ sở dữ liệu nghiệp vụ chính)
   * `training-db` (Cơ sở dữ liệu lưu trữ đặc trưng huấn luyện)
3. Nhấp vào nút **Actions** ở góc trên bên phải -> Chọn **Delete**.
4. Trong biểu mẫu xác nhận xóa:
   * **Bỏ tích chọn** mục *Create final snapshot?* (Tạo bản sao lưu cuối cùng - để tránh phát sinh chi phí lưu trữ snapshot).
   * **Bỏ tích chọn** mục *Retain automated backups* (Giữ lại các bản sao lưu tự động).
   * Tích chọn mục xác nhận: *I acknowledge that upon deletion, automated backups, including system snapshots and point-in-time recovery, will no longer be available.*
   * Nhập cụm từ `delete me` vào ô văn bản xác nhận ở cuối.
5. Nhấp nút **Delete** để hệ thống tiến hành giải phóng tài nguyên.

> [!WARNING]
> Việc xóa cơ sở dữ liệu RDS sẽ xóa sạch toàn bộ dữ liệu lịch sử giao dịch bán hàng, bảng đặc trưng `final_daily` và kết quả dự báo trong hệ thống. Hãy chắc chắn bạn đã trích xuất các bảng dữ liệu này ra file CSV cục bộ nếu cần lưu trữ kết quả báo cáo.

