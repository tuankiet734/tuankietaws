---
title: "Giao diện Cổng thông tin & Phân quyền"
date: 2024-07-07
weight : 7
chapter: false
pre: " <b> 5.7. </b> "
---

### 5.7. Giao diện Cổng thông tin & Phân quyền (Full-Stack Web App)

Trong Giai đoạn 4, chúng ta thiết kế và tích hợp giao diện người dùng quản trị doanh nghiệp chuyên sâu (**Global Fashion Retail Portal**). Hệ thống đảm bảo phân quyền người dùng chặt chẽ, xác thực hai lớp an toàn, và trực quan hóa dữ liệu thông minh trên nền tảng AWS.

---

#### 1. Cơ chế Truy xuất Dữ liệu Đa chế độ (DAL - Data Access Layer)

Để hệ thống hoạt động linh hoạt giữa các môi trường (phát triển cục bộ, kiểm thử, và chạy thực tế trên Cloud), lớp truy cập dữ liệu (`db.js`) ở Node.js backend hỗ trợ **3 chế độ hoạt động**:

*   **Chế độ REST API (API Mode):** Kết nối qua API Gateway tới lớp FastAPI Backend khi cấu hình biến môi trường `API_BASE_URL`. Các request HTTP kèm theo Header Authorization Bearer Token để xác thực.
*   **Chế độ PostgreSQL Trực tiếp (Real DB Mode):** Sử dụng driver `pg` tạo Connection Pool kết nối trực tiếp đến Amazon RDS PostgreSQL (`training-db` hoặc `fashion-rds`) thông qua cấu hình tệp `.env`.
*   **Chế độ Mock Cục bộ (Mock JSON Mode):** Cơ chế dự phòng (Fallback) tự động đọc/ghi dữ liệu vào các tệp JSON tĩnh lưu tại thư mục `data/` cục bộ khi không có kết nối API/Database.

##### Sơ đồ logic cấu hình đa chế độ:
```javascript
// db.js - Lớp trừu tượng dữ liệu đa chế độ
const fs = require('fs');
const { Pool } = require('pg');

let dbMode = 'mock';
let pool = null;

if (process.env.API_BASE_URL) {
    dbMode = 'api';
    console.log("Database Mode: REST API Client active");
} else if (process.env.DB_HOST) {
    dbMode = 'postgres';
    pool = new Pool({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        database: process.env.DB_NAME,
        password: process.env.DB_PASSWORD,
        port: process.env.DB_PORT
    });
    console.log("Database Mode: Direct PostgreSQL Connection Pool active");
} else {
    console.log("Database Mode: Local Mock JSON active");
}
```

---

#### 2. Hệ thống Xác thực Bảo mật Đa lớp (JWT & 2FA TOTP)

Hệ thống bảo vệ tài khoản người dùng bằng cơ chế đăng nhập mã hóa kết hợp xác thực đa yếu tố:

1.  **Token JWT:** Đăng nhập thành công sẽ cấp mã **JSON Web Token** lưu trữ thông tin định danh (username, role, store_id) có thời hạn sử dụng **8 giờ** để kiểm tra quyền truy cập ở API đầu cuối.
2.  **Xác thực 2 lớp TOTP (MFA):** 
    *   Sử dụng thuật toán băm mật mã HMAC-SHA1 và giải mã Base32 viết thuần bằng JavaScript (không dùng thư viện ngoài) để xác thực mã số OTP 6 chữ số thay đổi mỗi 30 giây.
    *   Tương thích hoàn toàn với các ứng dụng xác thực phổ biến như Google Authenticator, Microsoft Authenticator bằng cách sinh chuỗi khóa bí mật và mã QR (`otpauth://totp/`).
3.  **Audit Logs (Nhật ký Hệ thống):** Toàn bộ hành động đăng nhập (`LOGIN`, `LOGIN_MFA`), bật/tắt bảo mật (`MFA_ENABLE`, `MFA_DISABLE`) đều được ghi log chi tiết kèm IP và mốc thời gian để phục vụ kiểm toán an ninh thông tin.

---

#### 3. Phân quyền Người dùng dựa trên Vai trò (RBAC Matrix)

Hệ thống triển khai ma trận kiểm soát truy cập phân quyền nghiêm ngặt giữa **7 vai trò người dùng**:

| Vai trò | Phạm vi hiển thị | Các quyền hạn nghiệp vụ cốt lõi |
| :--- | :--- | :--- |
| **IT Admin** | Toàn cầu | `manage_users`, `manage_permissions`, `view_audit_logs`, `manage_inventory` |
| **Director** | Toàn cầu | Quyền tối cao (Xem toàn bộ Dashboard, Stores, Employees, Transactions của mọi cửa hàng) |
| **Finance/Auditor** | Toàn cầu | `view_all_stores`, `view_transactions`, `view_discounts`, `view_inventory` |
| **Inventory Manager** | Cửa hàng liên kết | `view_products`, `edit_products`, `view_inventory`, `manage_inventory` |
| **Marketing Manager** | Toàn cầu | `view_all_stores`, `view_discounts`, `edit_discounts`, `view_inventory` |
| **Store Manager** | Cửa hàng liên kết | Quản lý hóa đơn, sản phẩm, chiết khấu và thông tin nhân viên tại cửa hàng được gán |
| **Sales Staff** | Cửa hàng liên kết | Xem danh mục sản phẩm, tạo hóa đơn bán lẻ (`create_transaction`), thêm khách hàng |

> [!CAUTION]
> **Role Hierarchy (Thứ bậc quản trị):** Người dùng chỉ được quyền tạo hoặc chỉnh sửa các tài khoản có vai trò ngang hàng hoặc thấp hơn vai trò của mình, ngăn chặn tuyệt đối việc chiếm quyền điều khiển hệ thống hoặc tạo tài khoản vượt cấp.

---

#### 4. Dashboard Bản đồ Tương tác & Dự báo Nhu cầu (LightGBM Integration)

Giao diện Dashboard chính được thiết kế hiện đại và trực quan:

*   **Bản đồ số Mapbox GL JS:** Hiển thị vị trí địa lý của tất cả các cửa hàng bán lẻ toàn cầu dưới dạng các Marker tương tác.
*   **Skeleton Loader:** Màn hình chờ hiển thị quả địa cầu 3D tự quay mượt mà trong lúc tải dữ liệu bản đồ để tăng tính thẩm mỹ cao cấp.
*   **Panel Dự báo doanh số (Weekly Forecast):** Khi nhấp vào biểu tượng một cửa hàng bất kỳ:
    *   Hệ thống gọi API `/predict` để lấy dữ liệu dự báo từ mô hình **LightGBM** trên AWS.
    *   Sử dụng thư viện **Plotly.js** để vẽ đường đồ thị trực quan so sánh giữa số lượng bán **Thực tế (Actual)** và số lượng **Dự báo (Forecast)** theo tuần hoặc tháng.
*   **Cảnh báo hụt hàng (Inventory Shortage Alert):** Tự động đối chiếu lượng tồn kho thực tế với dự báo nhu cầu tuần tới. Nếu thiếu hụt, hệ thống sẽ nhấp nháy thanh thông báo cảnh báo màu đỏ kèm số lượng cụ thể cần bổ sung.

---

#### 5. Hoàn thiện các Tab Quản trị Dữ liệu Doanh nghiệp

*   **Customers:** Bảng danh sách khách hàng, công cụ tìm kiếm và vẽ biểu đồ Plotly thể hiện cơ cấu giới tính (Pie chart) và phân bố độ tuổi khách hàng (Histogram).
*   **Discounts:** Thống kê các chương trình khuyến mãi hiện hành và trực quan hóa tỷ lệ chiết khấu trung bình (`total_discount_avg`).
*   **Employees:** Quản lý nhân viên thuộc phạm vi phân quyền, kèm biểu đồ Plotly đánh giá doanh số đóng góp của từng nhân sự.
*   **Products:** Lưới hiển thị danh mục sản phẩm (Product Grid) tích hợp **hình ảnh sinh tự động từ mô hình GenAI Amazon Bedrock (Stable Diffusion/Titan)** được lưu trữ và truy xuất từ AWS S3.
*   **Stores:** Thống kê số lượng SKU hoạt động và thông tin vị trí các cửa hàng toàn cầu.
*   **Transactions:** Hiển thị lịch sử hóa đơn bán lẻ, bộ lọc nâng cao theo hình thức thanh toán, loại tiền tệ và quy đổi sang doanh thu USD tương đương.
*   **Inventory:** Xem và chỉnh sửa số lượng sản phẩm tồn kho thực tế theo từng store.

---

#### 6. Giao diện và thiết kế UI/UX (SPA)

*   **Kiến trúc SPA (Single Page Application):** Tải nội dung và dữ liệu không đồng bộ thông qua các hàm Fetch/AJAX, chuyển đổi các tab trên sidebar client-side mượt mà mà không cần tải lại toàn bộ trang.
*   **Đa ngôn ngữ (i18n):** Chuyển đổi ngôn ngữ linh hoạt giữa **Tiếng Việt 🇻🇳**, **Tiếng Anh 🇺🇸**, và **Tiếng Trung 🇨🇳** cho toàn bộ giao diện và đồ thị Plotly.
*   **Chế độ Sáng/Tối (Light/Dark Mode):** Sử dụng các CSS Variables điều khiển bảng màu HSL hài hòa, áp dụng hiệu ứng kính mờ (Glassmorphism) sang trọng để giảm mệt mỏi cho mắt người quản trị khi sử dụng lâu dài.
