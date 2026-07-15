---
title: "Xóa các S3 Buckets"
date: 2024-07-07
weight: 3
chapter: false
pre : " <b> 5.9.3. </b> "
---

### 5.9.3. Dọn dẹp và xóa các Amazon S3 Buckets

Amazon S3 yêu cầu tất cả các đối tượng (objects) bên trong bucket phải được làm rỗng hoàn toàn trước khi cho phép xóa chính bucket đó. Hãy thực hiện dọn dẹp theo quy trình sau:

1. Truy cập **Amazon S3 Console**.
2. Tìm và nhấp chọn S3 bucket lưu trữ mô hình học máy: `fashion-retail-model-storage` (hoặc các bucket chứa ảnh sản phẩm sinh bởi GenAI như `fashion-product-images-group3979`).
3. Nhấp vào nút **Empty** ở menu phía trên:
   * Nhập cụm từ `permanently delete` để xác nhận làm rỗng toàn bộ đối tượng bên trong bucket (bao gồm các file `.pkl` trong thư mục `models/`).
   * Nhấp chọn **Empty** để hoàn tất việc dọn dẹp tệp.
4. Trở lại danh sách Buckets, chọn bucket đã làm rỗng đó và nhấp nút **Delete**:
   * Nhập tên chính xác của bucket để xác nhận việc xóa hoàn toàn.
   * Nhấp chọn **Delete bucket** để giải phóng tài nguyên.

---

#### Minh chứng dọn dẹp Amazon S3:

![Delete S3](/images/5-Workshop/5.9-Resource-cleanup/delete-s3.png)

