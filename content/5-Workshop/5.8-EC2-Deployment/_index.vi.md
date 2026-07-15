---
title: "Triển khai Web App lên EC2"
date: 2024-07-07
weight : 8
chapter: false
pre: " <b> 5.8. </b> "
---

### 5.8. Triển khai Web Application lên AWS EC2

Mục tiêu của Giai đoạn 5 là đưa mã nguồn Web Application lên máy chủ Cloud Production (**Amazon EC2**) và kết nối đồng bộ toàn bộ các dịch vụ AWS đã triển khai ở các giai đoạn trước: Amazon RDS, AWS Lambda / API Gateway, Amazon S3 và Amazon Cognito.

---

#### BƯỚC 1: Khởi tạo EC2 Instance trên AWS Console

##### 1.1 Khởi chạy Instance (Launch Instance):
1. Truy cập **AWS Management Console**, tìm kiếm dịch vụ **EC2**.
2. Tại màn hình **EC2 Dashboard**, nhấp nút **Launch instance** màu cam.

##### 1.2 Cấu hình Tên và Hệ điều hành (AMI):
*   **Name:** Đặt tên máy chủ là `fashion-web-server`.
*   **Application and OS Images (AMI):** Chọn **Ubuntu**, chọn phiên bản **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type** (64-bit x86).

##### 1.3 Cấu hình Instance Type & Key Pair:
*   **Instance type:** Tìm và chọn loại instance `t3.large` (2 vCPUs, 8 GiB RAM) để đảm bảo hiệu năng xử lý tác vụ Web Portal và trực quan hóa Plotly mượt mà.
*   **Key pair:** Chọn key pair sẵn có hoặc bấm **Create new key pair** với định dạng `.pem` (đặt tên `fashion-key.pem`) để kết nối SSH.

##### 1.4 Thiết lập Security Group (Inbound Rules):
Tại mục **Network settings**, chọn **Create security group**, đặt tên là `web-app-sg` và cấu hình các rule Inbound như sau:

| Type | Protocol | Port Range | Source | Mục đích |
| :--- | :--- | :--- | :--- | :--- |
| **SSH** | TCP | `22` | `My IP` | Kết nối quản trị dòng lệnh bảo mật |
| **HTTP** | TCP | `80` | `0.0.0.0/0` | Tiếp nhận lưu lượng Web công khai |
| **HTTPS** | TCP | `443` | `0.0.0.0/0` | Tiếp nhận lưu lượng HTTPS mã hóa SSL |
| **Custom TCP** | TCP | `3000` | `10.0.0.0/16` | Node.js App chạy nội bộ trong VPC |
| **Custom TCP** | TCP | `8000` | `10.0.0.0/16` | REST API FastAPI chạy nội bộ trong VPC |

*   **Configure storage:** Thiết lập ổ đĩa SSD kích thước tối thiểu **20 GiB gp3** để đảm bảo tốc độ đọc/ghi dữ liệu và không gian cài đặt thư viện phần mềm.
*   Bấm **Launch instance** và đợi máy chủ chuyển sang trạng thái `Running`.

---

#### BƯỚC 2: Kết nối SSH vào EC2 và Cài đặt môi trường

##### 2.1 Kết nối SSH:
Mở PowerShell (Windows) hoặc Terminal (macOS/Linux) và di chuyển vào thư mục chứa key pair `.pem`:
```bash
# Cấp quyền đọc cho key pair (đối với macOS/Linux)
chmod 400 fashion-key.pem

# Kết nối SSH (Thay địa chỉ IP bằng Public IP thực của máy chủ EC2)
ssh -i "fashion-key.pem" ubuntu@<PUBLIC_IP_EC2>
```

##### 2.2 Cài đặt các công cụ nền tảng:
Sau khi đã SSH thành công vào máy chủ EC2 Ubuntu, chạy chuỗi lệnh sau để cài đặt Node.js 20.x, máy chủ Nginx, trình quản lý tiến trình PM2, PostgreSQL Client và AWS CLI:
```bash
# 1. Cập nhật danh sách gói và nâng cấp hệ thống
sudo apt update && sudo apt upgrade -y

# 2. Cài đặt Web Server Nginx
sudo apt install nginx -y

# 3. Thêm kho phần mềm Node.js 20.x và cài đặt
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# 4. Kiểm tra phiên bản cài đặt thành công
node -v   # Yêu cầu hiển thị v20.x.x
npm -v    # Yêu cầu hiển thị v10.x.x

# 5. Cài đặt toàn cục PM2 để quản lý tiến trình nền của Node.js
sudo npm install -g pm2

# 6. Cài đặt AWS CLI và công cụ truy vấn PostgreSQL client
sudo apt install awscli postgresql-client -y
```

---

#### BƯỚC 3: Deploy Mã nguồn và Cấu hình Biến môi trường (.env)

##### 3.1 Clone mã nguồn dự án:
```bash
# Tạo thư mục chứa ứng dụng
mkdir -p /home/ubuntu/app
cd /home/ubuntu/app

# Clone mã nguồn trực tiếp từ GitHub repository (thay thế URL tương ứng)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .
```

##### 3.2 Khởi tạo tệp cấu hình môi trường bảo mật (`.env`):
Tạo file `.env` bằng trình soạn thảo Nano:
```bash
nano .env
```
Nhập cấu hình kết nối thực tế của hệ thống:
```env
# ======= DATABASE – Amazon RDS =======
DB_HOST=training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=fashiondb
DB_USER=dbadmin
DB_PASSWORD=Tung2004

# ======= AWS SERVICES =======
AWS_REGION=ap-southeast-1
S3_BUCKET_NAME=fashion-retail-model-storage
API_GATEWAY_URL=https://5e0wzdirtc.execute-api.ap-southeast-1.amazonaws.com/dev

# ======= AUTHENTICATION =======
JWT_SECRET=fashion_secret_key_jwt_token_retail_portal_2026
COGNITO_USER_POOL_ID=ap-southeast-1_XXXXXXXX
COGNITO_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx

# ======= APP CONFIG =======
NODE_ENV=production
PORT=3000
```
*Nhấn `Ctrl + O` để lưu, và `Ctrl + X` để thoát.*

> [!CAUTION]
> Tuyệt đối không commit tệp cấu hình `.env` chứa mật khẩu cơ sở dữ liệu và mã bí mật lên hệ thống quản lý mã nguồn Git để bảo vệ an toàn thông tin đám mây.

##### 3.3 Cài đặt thư viện dependencies:
```bash
npm install --production
```

---

#### BƯỚC 4: Cấu hình PM2 để Khởi chạy ứng dụng liên tục

PM2 đảm bảo máy chủ Node.js chạy ngầm liên tục và tự động khởi động lại nếu ứng dụng gặp sự cố crash bất ngờ:

```bash
# Khởi động ứng dụng Express.js với tên tiến trình "fashion-web"
pm2 start app.js --name "fashion-web" --env production

# Kiểm tra danh sách tiến trình chạy nền (cột status phải hiển thị 'online' màu xanh lá)
pm2 list

# Thiết lập tự động kích hoạt lại PM2 khi máy chủ EC2 bị reboot hoặc khởi động lại
pm2 startup
```
*Lưu ý: Lệnh `pm2 startup` sẽ sinh ra một dòng mã lệnh `sudo env PATH=...` ở đầu ra màn hình. Bạn cần sao chép chính xác dòng lệnh đó và chạy trên terminal để hoàn tất đăng ký systemd.*

```bash
# Lưu trạng thái cấu hình hiện tại của PM2 để phục vụ khởi động lại
pm2 save
```

---

#### BƯỚC 5: Cấu hình Nginx làm Reverse Proxy

Nginx đóng vai trò là cổng tiếp nhận traffic HTTP (Cổng 80) bên ngoài internet, định tuyến luồng dữ liệu một cách an toàn vào ứng dụng Node.js nội bộ (Cổng 3000) và tối ưu hóa việc phân phát các tệp tin tĩnh.

##### 5.1 Khởi tạo tệp cấu hình Nginx riêng:
```bash
sudo nano /etc/nginx/sites-available/fashion-app
```
Dán cấu hình sau (thay thế tên miền của bạn nếu có, hoặc giữ nguyên Public IP):
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    client_max_body_size 20M;

    location / {
        proxy_pass         http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection 'upgrade';
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 90;
    }

    location /static {
        alias   /home/ubuntu/app/public;
        expires 30d;
    }
}
```

##### 5.2 Kích hoạt cấu hình và Khởi động lại Nginx:
```bash
# Tạo liên kết tượng trưng (symlink) để kích hoạt trang web
sudo ln -s /etc/nginx/sites-available/fashion-app /etc/nginx/sites-enabled/

# Xóa tệp cấu hình mặc định (default) của Nginx để tránh xung đột cổng 80
sudo rm /etc/nginx/sites-enabled/default

# Kiểm tra cú pháp cấu hình Nginx (yêu cầu báo: syntax is ok và test is successful)
sudo nginx -t

# Khởi động lại dịch vụ Nginx để áp dụng cấu hình mới
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

#### BƯỚC 6: Cài đặt Chứng chỉ bảo mật SSL/HTTPS với Certbot

Để bảo vệ đường truyền thông tin đăng nhập và dữ liệu giao dịch kinh doanh giữa trình duyệt và máy chủ, chúng ta cài đặt chứng chỉ SSL miễn phí từ tổ chức **Let's Encrypt**:

```bash
# Cài đặt certbot và module tích hợp nginx
sudo apt install certbot python3-certbot-nginx -y

# Đăng ký và cấu hình chứng chỉ SSL tự động (thay thế tên miền thực tế đã trỏ IP A record về EC2)
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Kiểm tra cơ chế tự động gia hạn chứng chỉ (SSL Let's Encrypt hết hạn sau 90 ngày)
sudo certbot renew --dry-run
```

---

#### BƯỚC 7: Kiểm tra liên hợp kết nối các Dịch vụ AWS

Sau khi cấu hình hoàn tất, thực hiện chạy các dòng lệnh sau để kiểm thử kết nối đầu cuối giữa máy chủ Web App EC2 và các tài nguyên đám mây khác:

##### 7.1 Kiểm tra kết nối RDS:
```bash
psql -h training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com \
     -U dbadmin -d fashiondb \
     -c "SELECT COUNT(*) FROM stores;"
```
*Kết quả mong đợi: Trả về số lượng stores thực tế trong DB.*

##### 7.2 Kiểm tra API Gateway & Lambda Forecast API:
```bash
curl -X POST https://5e0wzdirtc.execute-api.ap-southeast-1.amazonaws.com/dev/predict \
  -H "Content-Type: application/json" \
  -H "x-api-key: YEUnLELr4c4tqQdnToSw43sYJRqIKBrd5WDYxZH9" \
  -d '{"store_id":"20","sku":"FESH6946-S-","date":"2025-03-18"}'
```
*Kết quả mong đợi: API trả về mã thành công kèm số lượng dự báo doanh số.*

##### 7.3 Kiểm tra truy cập tệp ảnh S3:
```bash
aws s3 ls s3://fashion-retail-model-storage/models/ --region ap-southeast-1
```
*Kết quả mong đợi: Liệt kê đầy đủ 3 tệp pickle mô hình học máy.*

---

#### BƯỚC 8: Kiểm tra hoạt động toàn diện (End-to-End Test)

Mở trình duyệt, truy cập vào tên miền `https://your-domain.com` (hoặc IP Public của máy chủ EC2) và tiến hành kiểm tra hoạt động theo checklist phân quyền sau:

| Bước | Vai trò đăng nhập | Thao tác kiểm tra | Kết quả mong đợi |
| :--- | :--- | :--- | :--- |
| **8.1** | **Sales Staff** | Đăng nhập tài khoản Nhân viên bán hàng | Đăng nhập thành công, thanh menu chỉ hiển thị 2 Tab: *Transactions* và *Products*. |
| **8.2** | **Store Manager** | Đăng nhập tài khoản Quản lý cửa hàng | Đăng nhập thành công, hiển thị các tab quản trị. Chỉnh sửa thông tin *Discounts* hoặc *Employees* trong phạm vi cửa hàng hoạt động tốt. |
| **8.3** | **Director** | Đăng nhập tài khoản Giám đốc cấp cao | Đăng nhập thành công, hiển thị tab *Dashboard*. Bản đồ **Mapbox** tải thành công các Marker cửa hàng. Click vào Marker vẽ biểu đồ **Plotly** hiển thị đường so sánh số liệu Dự báo (Forecast) và Thực tế (Actual) thành công. |

---

#### PHỤ LỤC: Xử lý các sự cố thường gặp (Troubleshooting)

1.  **Lỗi `502 Bad Gateway`:**
    *   *Nguyên nhân:* Ứng dụng Node.js ở cổng 3000 đang bị dừng hoạt động hoặc crash mã nguồn.
    *   *Khắc phục:* Chạy lệnh `pm2 logs fashion-web` trên terminal EC2 để kiểm tra vết lỗi (Stack trace) và khởi động lại bằng `pm2 restart fashion-web`.
2.  **Lỗi kết nối Cơ sở dữ liệu RDS timeout:**
    *   *Nguyên nhân:* Security Group của RDS chưa mở quyền truy cập cổng 5432 cho IP hoặc Security Group của máy chủ EC2.
    *   *Khắc phục:* Vào RDS Dashboard -> Connectivity & security -> Nhấp vào VPC Security Groups, thêm rule Inbound cho phép cổng 5432 từ Security Group của `fashion-web-server`.
3.  **Hình ảnh sản phẩm trên tab Products bị lỗi link:**
    *   *Nguyên nhân:* Instance EC2 chưa được gán IAM Role có quyền đọc S3 hoặc bucket S3 chưa mở quyền truy cập ảnh.
    *   *Khắc phục:* Gán IAM Role có chính sách `AmazonS3ReadOnlyAccess` vào thực thể EC2 Web App, hoặc kiểm tra chính sách Bucket Policy trên S3.
4.  **Lỗi `403 Forbidden` khi gọi API dự báo:**
    *   *Nguyên nhân:* API Key truyền lên trong Header (`x-api-key`) bị sai hoặc thiếu.
    *   *Khắc phục:* Kiểm tra lại cấu hình biến môi trường `x-api-key` ở file cấu hình API Gateway của Node.js.
