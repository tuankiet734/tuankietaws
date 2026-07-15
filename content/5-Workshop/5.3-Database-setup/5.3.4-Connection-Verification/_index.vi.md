---
title: "Kiểm tra kết nối"
date: 2024-07-07
weight: 4
chapter: false
pre : " <b> 5.3.4. </b> "
---

### 5.3.4. Kiểm tra Kết nối và Thiết lập Bảng mẫu

Sau khi hoàn tất khởi động cơ sở dữ liệu và mở các cổng Security Group, bước tiếp theo là xác minh kết nối từ bên ngoài và tiến hành thiết lập cấu trúc bảng nghiệp vụ cơ bản.

---

#### Bước 1: Kiểm tra kết nối từ máy phát triển qua CLI (`psql`)

Chạy các lệnh psql sau trong terminal để đảm bảo đường truyền thông suốt:

##### Kết nối tới Central DB (cơ sở dữ liệu nghiệp vụ):
```bash
psql -h fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com -p 5432 -U dbadmin -d fashiondb
```

##### Kết nối tới Training DB (cơ sở dữ liệu lưu trữ đặc trưng):
```bash
psql -h training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com -p 5432 -U dbadmin -d fashiondb
```
*(Sau khi chạy lệnh, nhập mật khẩu của bạn để kiểm tra dấu nhắc lệnh)*

---

#### Bước 2: Thiết lập bảng mẫu trên Central DB (`fashion-rds`)

Sau khi kết nối thành công (sử dụng DBeaver, pgAdmin hoặc CLI), chạy tập lệnh SQL sau trên `fashion-rds` để khởi tạo các bảng nghiệp vụ chính:

```sql
-- 1. Bảng sản phẩm (products)
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2)
);

-- 2. Bảng cửa hàng (stores)
CREATE TABLE stores (
    store_id VARCHAR(50) PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(50)
);

-- 3. Bảng lịch sử giao dịch (transactions)
CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    store_id VARCHAR(50) REFERENCES stores(store_id),
    product_id VARCHAR(50) REFERENCES products(product_id),
    date DATE,
    qty INT
);
```

Các dữ liệu thô này sẽ được công cụ ETL (AWS Glue) trích xuất hàng ngày để xử lý.

---

#### Minh chứng thực tế trên AWS Console:
Dưới đây là hình ảnh xác minh kết nối cơ sở dữ liệu qua DBeaver:

![DBeaver Connections](/images/5-Workshop/5.3-Database-setup/dbeaver-connections.png)