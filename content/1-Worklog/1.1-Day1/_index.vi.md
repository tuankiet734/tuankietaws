---
title: "Ngày 1"
date: 2026-06-01
weight: 1
chapter: false
pre: " <b> 1.1. </b> "
---

# Nhật Ký Làm Việc: Khởi Tạo Tài Khoản, Tích Lũy Credit và Thực Hành Các Dịch Vụ Cốt Lõi

> **Ngày 1 - Thứ Hai, ngày 01/06/2026:** Kích hoạt tài khoản học tập AWS, nhận credit khởi đầu và hoàn thành 5 bài thực hành hướng dẫn trên console để nhận thêm credit khuyến mãi.

---

### Mục tiêu học tập trong ngày

- Đăng ký thành công tài khoản AWS cá nhân và nhận **$100 credit ban đầu** từ chương trình.
- Thực hiện **5 bài thực hành hướng dẫn** trên AWS Console để kiếm thêm **$100 credit** ($20 cho mỗi bài hoàn thành).
- Trực tiếp làm quen với giao diện và cách hoạt động của 5 dịch vụ AWS cơ bản: EC2, Bedrock, Budgets, Lambda, và RDS.
- Hiểu rõ nguyên tắc quản lý chi phí và quy trình dọn dẹp tài nguyên sau khi thực hành.

---

### Task 1: Khởi tạo máy chủ ảo EC2 (Nhận +$20 Credit)

**Mục tiêu:** Khởi tạo, kiểm tra và quản lý một máy chủ ảo (Virtual Machine) trên hạ tầng AWS.

**Giới thiệu dịch vụ:** **Amazon EC2 (Elastic Compute Cloud)** cung cấp tài nguyên điện toán đám mây có thể mở rộng, cho phép người dùng cấu hình hệ điều hành, RAM, CPU và các thiết lập bảo mật mạng linh hoạt.

**Quy trình thực hiện:**
1. Trên giao diện **AWS Console** → tìm widget **Explore AWS** ở trang chủ → chọn bài thực hành **Launch an instance using EC2**.
2. Chọn **Start activity** để bắt đầu lab.
3. Cấu hình máy chủ ảo:
   - Tên máy chủ (Name tag): `FCA-Test-Server`
   - Hệ điều hành (AMI): Chọn Amazon Linux 2023 (thuộc diện Free Tier).
   - Cấu hình phần cứng: Giữ cấu hình mặc định siêu nhỏ (`t2.micro` hoặc `t3.micro`).
4. Tạo cặp khóa bảo mật (Key Pair) để kết nối từ xa:
   - Tên khóa: `fca-keypair`
   - Loại khóa: **RSA**
   - Định dạng tệp: **.pem** (tải về lưu trữ an toàn trên máy cá nhân).
5. Tạo Nhóm bảo mật (Security Group) với các quy tắc tường lửa mặc định.
6. Xác nhận lại toàn bộ thông tin cấu hình và nhấn **Launch Instance**.
7. **Bước kiểm tra:** Truy cập danh sách EC2 để xác nhận máy chủ đã chuyển sang trạng thái **Running** và vượt qua cả **2/2 status checks**.
8. **Dọn dẹp hệ thống (Bắt buộc):** Chọn máy chủ vừa tạo → Instance State → Chọn **Terminate Instance** để xóa bỏ hoàn toàn máy ảo này.

> **Bài học kinh nghiệm:** Việc khởi tạo tài nguyên rất nhanh chóng nhưng sẽ tính phí liên tục. Sau khi kiểm tra xong, cần terminate máy chủ ngay lập tức và đảm bảo ổ cứng EBS đi kèm cũng được xóa để tránh phát sinh chi phí ngoài ý muốn.

---

### Task 2: Thử nghiệm Promt trên Bedrock Playground (Nhận +$20 Credit)

**Mục tiêu:** Trải nghiệm khả năng tương tác với các mô hình trí tuệ nhân tạo (Generative AI) trên hạ tầng AWS.

**Giới thiệu dịch vụ:** **Amazon Bedrock** cung cấp giao thức kết nối thống nhất đến các mô hình ngôn ngữ lớn (LLM) hàng đầu từ các nhà phát triển lớn (như Anthropic, Meta, Cohere) thông qua API mà không đòi hỏi người dùng quản lý phần cứng.

**Quy trình thực hiện:**
1. Truy cập **Amazon Bedrock Console** → chọn bài thực hành **Use a foundation model in Amazon Bedrock**.
2. Tìm đến mục đăng ký quyền truy cập mô hình và chọn **Claude 3 Haiku** (mô hình có tốc độ phản hồi nhanh và tối ưu chi phí).
3. Nếu hệ thống báo chưa được phân quyền, thực hiện điền thông tin mô tả mục đích sử dụng (Use case) ngắn gọn và gửi yêu cầu kích hoạt.
4. Khi quyền truy cập đã được duyệt, vào giao diện **Text Playground** và chọn mô hình **Claude 3 Haiku**.
5. Nhập nội dung thử nghiệm (ví dụ: "Tóm tắt 3 lợi ích cốt lõi của điện toán đám mây") và chọn **Run**.
6. Theo dõi kết quả phản hồi, thử thay đổi thông số cấu hình như Temperature (độ sáng tạo của văn bản) và nhấn **Finish** để hoàn tất nhiệm vụ.

> **Bài học kinh nghiệm:** Việc truy cập các mô hình AI trên AWS yêu cầu tuân thủ chính sách AI có trách nhiệm (Responsible AI). Việc cung cấp lý do sử dụng rõ ràng sẽ giúp yêu cầu mở khóa dịch vụ được phê duyệt nhanh chóng hơn.

---

### Task 3: Cấu hình hạn mức chi tiêu với AWS Budgets (Nhận +$20 Credit)

**Mục tiêu:** Xây dựng hàng rào cảnh báo chi phí tự động để kiểm soát lượng credit được cấp.

**Giới thiệu dịch vụ:** **AWS Budgets** giám sát chi phí sử dụng dịch vụ và tự động gửi thông báo qua Email hoặc SMS khi chi phí thực tế hoặc dự báo vượt quá hạn mức thiết lập.

**Quy trình thực hiện:**
1. Vào **AWS Billing Console** → chọn mục **Budgets** → chọn bài thực hành **Set up a cost budget using AWS Budgets**.
2. Nhấn **Start activity** để mở trình hướng dẫn tạo ngân sách.
3. Thiết lập thông số:
   - Loại ngân sách: Cost Budget (Theo dõi chi phí).
   - Chu kỳ: Monthly (Hàng tháng).
   - Hạn mức ngân sách (Budgeted Amount): $20.00.
4. Cài đặt ngưỡng cảnh báo:
   - Thiết lập gửi cảnh báo khi chi phí thực tế chạm mức **80% ($16.00)** của hạn mức.
   - Nhập địa chỉ email cá nhân để nhận thông báo khẩn cấp.
5. Kiểm tra thông tin cấu hình và nhấn **Create budget** để kích hoạt.

> **Bài học kinh nghiệm:** Cấu hình ngân sách là bước bảo vệ tài khoản đầu tiên cần làm. Cảnh báo sớm giúp phát hiện kịp thời các dịch vụ chạy ngầm trước khi chúng tiêu thụ hết số credit của tài khoản.

---

### Task 4: Triển khai Web App không máy chủ với AWS Lambda (Nhận +$20 Credit)

**Mục tiêu:** Lập trình và chạy mã nguồn ứng dụng trên mô hình Serverless.

**Giới thiệu dịch vụ:** **AWS Lambda** thực thi mã nguồn dựa trên sự kiện kích hoạt (như yêu cầu HTTP) và tự động quản lý hạ tầng phần cứng bên dưới. Chi phí chỉ tính trên thời gian xử lý thực tế, khi không có yêu cầu hệ thống sẽ không tốn phí.

**Quy trình thực hiện:**
1. Truy cập **AWS Lambda Console** → chọn bài thực hành **Create a web app using AWS Lambda**.
2. Nhấp **Start activity** → chọn **Use a blueprint** (sử dụng mẫu dựng sẵn) → tìm mẫu **Getting started with Lambda HTTP**.
3. Cấu hình hàm xử lý:
   - Tên hàm (Function name): `fca-http-lambda-app`
   - Đánh dấu đồng ý tạo vai trò IAM mới với các quyền cơ bản phục vụ thực thi hàm.
4. Nhấn **Create function** và chờ hệ thống triển khai xong.
5. **Kiểm tra hoạt động:** Sao chép đường dẫn **Function URL** được cấp, mở tab mới trên trình duyệt và dán vào để kiểm tra xem hàm có trả về chuỗi kết quả chào mừng định dạng JSON hay không.
6. **Dọn dẹp:** Thực hiện xóa hàm (Delete) để làm sạch không gian làm việc.

> **Bài học kinh nghiệm:** Serverless giúp lập trình viên không cần bận tâm đến việc vá lỗi hay cấu hình hệ điều hành máy chủ. Khi không có lượt truy cập, chi phí vận hành ứng dụng sẽ bằng 0.

---

### Task 5: Tạo Cơ sở dữ liệu quan hệ được quản lý qua RDS (Nhận +$20 Credit)

**Mục tiêu:** Thiết lập và quản lý một cụm cơ sở dữ liệu quan hệ (Relational Database) an toàn.

**Giới thiệu dịch vụ:** **Amazon RDS** tự động hóa các tác vụ quản trị cơ sở dữ liệu phức tạp như sao lưu dự phòng, vá lỗi phần mềm hệ thống và thiết lập cơ chế dự phòng chống sự cố.

**Quy trình thực hiện:**
1. Vào **Amazon RDS Console** → chọn bài thực hành **Create an Amazon RDS Database**.
2. Sử dụng chế độ **Easy create** để áp dụng cấu hình tối ưu dựng sẵn.
3. Thiết lập thông số:
   - Động cơ cơ sở dữ liệu (Database Engine): **Aurora (PostgreSQL Compatible)**.
   - Loại máy chủ: Chọn kích thước tài nguyên nhỏ nhất có thể.
4. Nhấn **Create database** và chờ trạng thái của cơ sở dữ liệu chuyển sang **Available**.
5. **Quy trình dọn dẹp (Lưu ý thứ tự thực hiện):**
   - Không thể xóa trực tiếp Cluster nếu còn instance hoạt động bên trong.
   - Đầu tiên, chọn và thực hiện xóa DB instance (`database-1-instance-1`), bỏ chọn phần tạo snapshot cuối kỳ để hoàn thành nhanh.
   - Sau khi instance được xóa xong, tiến hành xóa Cluster cha (`database-1`).

> **Bài học kinh nghiệm:** Cơ sở dữ liệu quan hệ trên AWS có quy định nghiêm ngặt về chuỗi ràng buộc phụ thuộc. Cần xóa các instance con bên trong trước khi xóa cấu trúc cụm dữ liệu bên ngoài.

---

### Tổng kết Ngày 1 & Bài học rút ra

- **Tích lũy Credit:** Nhận thành công $100 credit ban đầu và kiếm thêm $100 qua việc hoàn tất 5 nhiệm vụ thực hành (Tổng cộng tài khoản có **$200**).
- **Trải nghiệm thực tiễn:** Tiếp cận trực tiếp cách vận hành của các dịch vụ cốt lõi: từ máy ảo (EC2), dịch vụ AI (Bedrock), hệ thống cảnh báo (Budgets), kiến trúc serverless (Lambda) đến cơ sở dữ liệu (RDS).
- **Ý thức tiết kiệm:** Rèn luyện thói quen kiểm tra và xóa bỏ tài nguyên ngay sau khi học xong. Việc quên tắt một DB instance hay máy chủ ảo có thể làm cạn kiệt lượng credit nhanh chóng.
- **Tiếp cận chủ động:** Tận dụng các bài thực hành có sẵn trên AWS Console là cách tốt nhất và an toàn nhất để tìm hiểu cách hoạt động của một dịch vụ cloud mới.

---

*Nguồn tài liệu chính: [First Cloud Journey - AWS Study Group](https://cloudjourney.awsstudygroup.com/)*
