---
title: "Ngày 2"
date: 2026-06-08
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
---

# Nhật Ký Làm Việc: Giám Sát Chi Phí Nâng Cao, Thiết Lập Cảnh Báo Đa Lớp và Lý Thuyết Hạ Tầng Cơ Bản

> **Ngày 2 - Thứ Hai, ngày 08/06/2026:** Hoàn thành xây dựng hệ thống cảnh báo chi phí đa tầng, thiết lập quy trình xử lý khẩn cấp và nghiên cứu sâu các lý thuyết kiến trúc đám mây và an toàn thông tin trên AWS.

---

### Mục tiêu học tập trong ngày

- Triển khai **Hệ thống giám sát chi phí đa lớp** nhằm chủ động ngăn ngừa phát sinh chi phí.
- Kích hoạt dịch vụ **Cost Anomaly Detection** kết hợp quy định gắn thẻ tag tài nguyên đồng bộ.
- Xây dựng tài liệu hướng dẫn **Quy trình xử lý chi phí khẩn cấp** bằng các lệnh tra cứu AWS CLI.
- Nghiên cứu lý thuyết hạ tầng cốt lõi của AWS: Mô hình trách nhiệm chung, Hạ tầng toàn cầu, IAM, các loại hình dịch vụ lưu trữ và điện toán.

---

### Hệ Thống Giám Sát Chi Phí & Hàng Rào Cảnh Báo

#### 1. Thiết lập 3 mức ngân sách với AWS Budgets

Để kiểm soát chặt chẽ lượng credit sử dụng, tôi đã thiết lập 3 ngân sách khác nhau trên bảng quản trị chi phí:

| Tên ngân sách cảnh báo | Ngưỡng giới hạn | Điều kiện kích hoạt cảnh báo |
|---|---|---|
| **Monthly Cap Budget** | $40.00 / tháng | Cảnh báo khi chi phí thực tế đạt **80% ($32.00)** |
| **Warning Budget** | $20.00 / tháng | Cảnh báo khi chi phí thực tế đạt **50% ($10.00)** |
| **Daily Safeguard Budget** | $5.00 / ngày | Cảnh báo khi chi phí thực tế đạt **100% ($5.00)** |

Ngân sách theo ngày đóng vai trò như một chốt chặn nhanh, giúp phát hiện sớm các tài nguyên cấu hình sai hoặc chạy ngầm trong vòng 24 giờ thay vì đợi cộng dồn đến cuối tháng.

#### 2. Cảnh báo chi phí leo thang qua CloudWatch Billing Alarms

Tôi đã thiết lập các Billing Alarm trong CloudWatch sử dụng Amazon SNS để gửi thông báo khẩn cấp theo các mức độ nghiêm trọng:

| Ngưỡng chi phí | Kênh nhận thông báo | Hành động vận hành |
|---|---|---|
| **$15.00** | Email cá nhân | Cảnh báo thông thường; kiểm tra danh sách dịch vụ đang chạy. |
| **$35.00** | Email + SMS điện thoại | Ưu tiên cao; kiểm tra chi tiết trạng thái hoạt động của tài nguyên. |
| **$60.00** | Email + SMS + Webhook Discord | Cảnh báo khẩn cấp; bắt đầu quy trình tắt tài nguyên khẩn cấp. |

#### 3. Tự động phát hiện bất thường bằng AWS Cost Anomaly Detection (Tính năng bổ sung mới)

Kích hoạt dịch vụ **AWS Cost Anomaly Detection** sử dụng thuật toán máy học (Machine Learning) để giám sát và phát hiện các chi tiêu bất thường dựa trên lịch sử sử dụng trước đó:
- Loại giám sát: Theo dõi toàn bộ các dịch vụ AWS.
- Ngưỡng kích hoạt: Chi phí bất thường vượt quá $5.00 trong ngày.
- Vai trò: Gửi thông báo ngay lập tức khi phát hiện biến động chi phí đột biến mà không cần đợi chạm ngưỡng ngân sách tĩnh.

---

### Phân Tích Chi Phí Nâng Cao & Gắn Thẻ Tài Nguyên

#### Chính sách gắn thẻ tag tài nguyên (Resource Tagging)

Để thuận tiện cho việc lập báo cáo và phân bổ ngân sách trong AWS Cost Explorer, mọi tài nguyên khởi tạo đều bắt buộc phải gắn các thẻ tag phân loại rõ ràng:

| Thẻ khóa (Tag Key) | Giá trị ví dụ | Ý nghĩa và mục đích |
|---|---|---|
| `Project` | `cloud-training` | Phân loại chi phí theo từng dự án cụ thể. |
| `Environment` | `dev` / `testing` | Phân biệt tài nguyên phòng Lab thử nghiệm và môi trường kiểm thử. |
| `Author` | `intern-dev` | Xác định kỹ sư chịu trách nhiệm khởi tạo và quản lý tài nguyên. |

#### Bảng điều khiển CloudWatch giám sát tập trung

- Thiết lập một **Bảng điều khiển giám sát (Dashboard)** trong CloudWatch hiển thị đồng thời biểu đồ CPU của EC2 và dự báo chi phí ước tính trong tháng.
- Theo dõi các số liệu cấp ứng dụng để phòng ngừa trường hợp vòng lặp vô hạn trong code thử nghiệm gây tốn tài nguyên.

---

### Quy Trình Xử Lý Chi Phí Khẩn Cấp & Dọn Dẹp Tài Nguyên

#### 1. Các lệnh tra cứu khẩn cấp qua AWS CLI

Khi nhận được cảnh báo chi phí bất thường, thực hiện ngay các lệnh CLI sau trên Terminal để quét và phát hiện các dịch vụ đang chạy gây tốn phí:

```bash
# 1. Liệt kê các máy chủ ảo EC2 đang chạy trong khu vực (Region) hiện tại
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].{ID:InstanceId,Type:InstanceType,Zone:Placement.AvailabilityZone}' \
  --output table

# 2. Liệt kê toàn bộ các cơ sở dữ liệu RDS đang hoạt động
aws rds describe-db-instances \
  --query 'DBInstances[].{DBIdentifier:DBInstanceIdentifier,Engine:Engine,Status:DBInstanceStatus}' \
  --output table

# 3. Tìm các ổ cứng EBS đang rảnh rỗi (vẫn bị tính phí ngay cả khi máy chủ đã tắt)
aws ec2 describe-volumes --filters "Name=status,Values=available" \
  --query 'Volumes[].{VolumeID:VolumeId,Size:Size,Zone:AvailabilityZone}' \
  --output table

# 4. Tìm các địa chỉ IP tĩnh (Elastic IP) không gắn với máy chủ nào (bị tính phí treo máy)
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].{IP:PublicIp,AllocationId:AllocationId}' \
  --output table
```

#### 2. Quy trình xử lý khẩn cấp từng bước
1. Đăng nhập ngay vào AWS Console bằng tài khoản quản trị.
2. Dừng (Stop) hoặc xóa hoàn toàn (Terminate) các máy chủ ảo `EC2` và xóa các cụm dữ liệu `RDS` không sử dụng.
3. Tiến hành xóa các ổ cứng `EBS` đang ở trạng thái `available` và giải phóng (Release) các địa chỉ `Elastic IP` đang rỗi.
4. Tắt các cấu hình thử nghiệm mô hình AI trên Bedrock và dọn dẹp các đường dẫn hàm Lambda cũ.

---

### Lý Thuyết Kiến Trúc Đám Mây Nền Tảng

#### Mô hình dịch vụ điện toán đám mây
- **Elasticity (Tính co giãn):** Khả năng tự động tăng hoặc giảm tài nguyên tùy theo lưu lượng truy cập thực tế.
- **Dịch chuyển chi phí:** Chuyển đổi từ chi phí đầu tư hạ tầng ban đầu (CapEx) sang chi phí vận hành trả theo mức sử dụng (OpEx).
- **Hạ tầng toàn cầu:** Khả năng triển khai ứng dụng đến các vùng địa lý khác nhau trên thế giới một cách nhanh chóng.

| Mô hình dịch vụ | Ví dụ trên AWS | Phần người dùng tự quản lý |
|---|---|---|
| **IaaS (Hạ tầng như một dịch vụ)** | Amazon EC2, VPC | Hệ điều hành, thư viện chạy code, mã nguồn ứng dụng và cấu hình mạng. |
| **PaaS (Nền tảng như một dịch vụ)** | AWS Elastic Beanstalk, RDS | Mã nguồn ứng dụng và cấu trúc bảng dữ liệu. |
| **SaaS (Phần mềm như một dịch vụ)** | Amazon WorkMail, Chime | Không cần quản lý hạ tầng; sử dụng phần mềm trực tiếp qua trình duyệt/ứng dụng. |

#### Hạ tầng toàn cầu của AWS
- **Regions (Vùng địa lý):** Các khu vực địa lý độc lập chứa nhiều trung tâm dữ liệu. Dữ liệu sẽ lưu trữ cố định tại Region đã chọn trừ khi được người dùng cấu hình sao chép đi nơi khác.
- **Availability Zones (AZs):** Các trung tâm dữ liệu vật lý riêng biệt trong một Region, kết nối bằng mạng cáp quang tốc độ cao. Triển khai tài nguyên trên nhiều AZ giúp hệ thống có **Độ sẵn sàng cao (High Availability)**.
- **Edge Locations (Điểm phân phối):** Điểm đặt máy chủ bộ nhớ đệm thuộc mạng lưới CDN CloudFront của AWS, giúp truyền tải nội dung tĩnh đến người dùng ở vị trí gần nhất với độ trễ thấp nhất.

---

### Bảo Mật Hệ Thống & Quản Lý Danh Tính (IAM)

- **Mô hình trách nhiệm chung (Shared Responsibility Model):**
  - **Trách nhiệm của AWS (OF the cloud):** Bảo mật hạ tầng vật lý của trung tâm dữ liệu, thiết bị mạng, phần cứng máy chủ và lớp ảo hóa.
  - **Trách nhiệm của khách hàng (IN the cloud):** Bảo mật hệ điều hành, cấu hình tường lửa (Security Group), phân quyền truy cập người dùng và mã hóa dữ liệu.
- **Nguyên tắc quản trị IAM:**
  - **Bảo vệ tài khoản Root:** Kích hoạt xác thực 2 lớp (MFA) và hạn chế sử dụng tài khoản Root cho công việc hàng ngày.
  - **Nguyên tắc quyền tối thiểu (Least Privilege):** Chỉ cấp đúng và đủ những quyền hạn cần thiết để thực hiện công việc.
  - **Quản lý theo Nhóm (Groups):** Gán quyền thông qua IAM Group thay vì phân quyền riêng lẻ cho từng người dùng.
  - **Cấu hình bằng JSON:** Sử dụng cấu trúc tài liệu JSON để mô tả chi tiết các hành động (Actions), tài nguyên (Resources) và điều kiện (Conditions) được phép truy cập.

---

### Tổng Quan Các Dịch Vụ Lưu Trữ & Cơ Sở Dữ Liệu

- **Amazon S3 (Simple Storage Service):**
  - Dịch vụ lưu trữ đối tượng với độ bền vững dữ liệu đạt **99.999999999% (11 số 9)**.
  - Hỗ trợ phân lớp lưu trữ (S3 Standard, Standard-IA, Glacier) để tối ưu hóa chi phí dựa trên tần suất truy xuất tệp tin.
- **Amazon RDS:** Cơ sở dữ liệu quan hệ được quản lý tự động, hỗ trợ sao lưu dự phòng định kỳ, vá lỗi bảo mật phần mềm và đồng bộ bản sao.
- **AWS Lambda:** Dịch vụ serverless thực thi code theo sự kiện, tự động mở rộng tài nguyên và không yêu cầu quản lý máy chủ.

---

### Nội Dung Học Tập Đã Hoàn Thành

| Ngày học | Nội dung bài học tập trung | Dịch vụ AWS liên quan |
|---|---|---|
| **08/06/2026** | Hạ tầng và cấu hình máy chủ ảo | Amazon EC2, AMI, Instance Types |
| **08/06/2026** | Phân quyền truy cập hệ thống | AWS IAM, Roles, Policies |
| **08/06/2026** | Môi trường lập trình tích hợp | AWS Cloud9, Instance Profiles |
| **08/06/2026** | Lưu trữ đối tượng và lưu trữ web tĩnh | Amazon S3, S3 Bucket Policies |
| **08/06/2026** | Cơ sở dữ liệu và quy trình sao lưu | Amazon RDS, DB Engines |

---

### Bài học rút ra từ Ngày 2

1. **Phòng thủ chi phí nhiều lớp:** Việc kết hợp ngân sách tĩnh (Budgets), cảnh báo chi phí (Alarms) và giám sát thông minh (Anomaly Detection) giúp bảo vệ tài khoản tối đa trước các rủi ro phát sinh hóa đơn lớn.
2. **Kỷ luật tagging:** Gắn thẻ tag tài nguyên là điều kiện bắt buộc để quản lý tài chính đám mây hiệu quả.
3. **Kỹ năng xử lý khẩn cấp:** Xây dựng sẵn kịch bản dọn dẹp và sử dụng các lệnh CLI để nhanh chóng quét các tài nguyên rác (như ổ cứng EBS chưa dùng hay IP tĩnh chưa gắn máy chủ) là kỹ năng vận hành thực tế cực kỳ quan trọng đối với kỹ sư đám mây.

---

*Nguồn tài liệu chính: [First Cloud Journey - AWS Study Group](https://cloudjourney.awsstudygroup.com/)*
