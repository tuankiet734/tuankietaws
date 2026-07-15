---
title: "Cấu hình Mạng và Bảo mật"
date: 2024-07-07
weight: 3
chapter: false
pre : " <b> 5.3.3. </b> "
---

### 5.3.3. Cấu hình Mạng và Bảo mật (Security & Network Groups)

Để đảm bảo an toàn tối đa cho dữ liệu doanh nghiệp đồng thời cho phép các thành phần khác kết nối, cấu hình bảo mật được thiết lập chặt chẽ thông qua các quy tắc của **VPC Security Group**:

* **Mã hóa lưu trữ (Storage Encryption):** Bật mã hóa ổ đĩa cho cả hai cơ sở dữ liệu sử dụng khóa mặc định của **AWS KMS** (`fe12be50-a2cf-44d1-a1da-3ce27e40686d`).
* **Security Group định tuyến cổng:** `sg-0fecd1d2df90f2a69`

---

#### Hướng dẫn chi tiết cấu hình Inbound Rules cho RDS:

1. **Mở EC2 Console:** Trên thanh công cụ AWS Console, truy cập dịch vụ **EC2**.
2. **Chọn Security Groups:** Nhấp vào **Security Groups** trong mục **Network & Security** ở menu điều hướng bên trái.
3. **Tìm kiếm Security Group:** Chọn Security Group tương ứng của RDS instance (ví dụ: `sg-0fecd1d2df90f2a69`).
4. **Chỉnh sửa Inbound Rules:** Nhấp chọn tab **Inbound rules** ở nửa dưới màn hình và bấm nút **Edit inbound rules**.
5. **Cấu hình 3 quy tắc kết nối bắt buộc:**
   * **Quy tắc 1 (Truy cập của nhà phát triển):** 
     * **Type:** Chọn `PostgreSQL` (Cổng mặc định `5432`).
     * **Source:** Chọn **My IP** (Tự động điền IP public hiện tại của máy tính bạn). Quy tắc này cho phép pgAdmin/DBeaver kết nối trực tiếp.
   * **Quy tắc 2 (Truy cập từ Máy chủ huấn luyện EC2):**
     * **Type:** Chọn `PostgreSQL` (Cổng mặc định `5432`).
     * **Source:** Chọn **Custom** và nhập mã ID Security Group của máy chủ `ML-Forecast-Server` (`sg-0579af9926812195b`).
   * **Quy tắc 3 (Truy cập cho AWS Glue kết nối JDBC):**
     * **Type:** Chọn `PostgreSQL` (Cổng mặc định `5432`).
     * **Source:** Chọn **Custom** và nhập lại chính mã ID Security Group này (`sg-0fecd1d2df90f2a69` - Self-referencing rule).
6. **Lưu cấu hình:** Nhấp vào nút **Save rules** để áp dụng.

---

#### Minh chứng hoạt động trên AWS Console:

Dưới đây là hình ảnh cấu hình luật Inbound Rules của Security Group trên AWS Management Console:

![Security Group Inbound Rules](/images/5-Workshop/5.3-Database-setup/security-group-inbound-rules.png)