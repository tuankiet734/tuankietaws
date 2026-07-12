---
title: "Kiểm tra kết nối"
date: 2024-07-07
weight: 4
chapter: false
pre: " <b> 5.2.4. </b> "
---

### 5.2.4. Kiểm tra Kết nối Cơ sở dữ liệu

Sau khi khởi tạo và cấu hình Security Group thành công, chúng ta cần xác minh kết nối đến cơ sở dữ liệu để đảm bảo các tiến trình phía sau không bị gián đoạn.

#### Cách 1: Sử dụng công cụ Command Line (`psql`)
Bạn có thể kết nối trực tiếp đến PostgreSQL shell bằng cách chạy các lệnh dưới đây từ terminal máy cá nhân:

##### Kết nối tới Central DB:
```bash
psql -h fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com -p 5432 -U dbadmin -d fashiondb
```

##### Kết nối tới Training DB:
```bash
psql -h training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com -p 5432 -U dbadmin -d fashiondb
```

Sau khi nhập mật khẩu đăng nhập, nếu shell hiển thị dấu nhắc lệnh `fashiondb=>` tức là kết nối thành công.

---

#### Cách 2: Sử dụng DBeaver hoặc pgAdmin
1. Mở công cụ quản trị Database Client của bạn.
2. Tạo kết nối mới (New Connection) chọn **PostgreSQL**.
3. Điền thông tin kết nối:
   * **Host:** Điền endpoint tương ứng của database.
   * **Port:** `5432`
   * **Database:** `fashiondb`
   * **Username:** `dbadmin`
   * **Password:** Mật khẩu tài khoản database.
4. Bấm **Test Connection** để kiểm tra. Nếu hiển thị trạng thái kết nối thành công, bấm **Finish** để lưu cấu hình.
