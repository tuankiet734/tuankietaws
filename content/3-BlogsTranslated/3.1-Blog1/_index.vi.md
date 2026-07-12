---
title: "Blog 1"
date: 2026-06-24
weight: 1
chapter: false
pre: " <b> 3.1. </b> "
---

# Xây dựng Offline Feature Store trên AWS: Tái sử dụng dữ liệu ML hiệu quả hơn

> **Bài gốc:** [Build an offline feature store using Amazon SageMaker Unified Studio and SageMaker Catalog](https://aws.amazon.com/blogs/machine-learning/build-an-offline-feature-store-using-amazon-sagemaker-unified-studio-and-sagemaker-catalog/)

> **Bài dịch:** [Build an offline feature store using Amazon SageMaker Unified Studio and SageMaker Catalog](#)

---

Trong các dự án Machine Learning, việc nhiều nhóm tự tạo và lưu trữ các feature riêng biệt thường dẫn đến tình trạng dữ liệu bị trùng lặp, khó quản lý và thiếu tính nhất quán. Điều này không chỉ làm tăng chi phí vận hành mà còn kéo dài thời gian phát triển mô hình.

---

## 1. Giải pháp mới từ AWS

AWS giới thiệu cách xây dựng **Offline Feature Store** bằng **Amazon SageMaker Unified Studio** và **SageMaker Catalog**, cho phép lưu trữ, quản lý và chia sẻ các feature ML trong một môi trường tập trung.

Thay vì mỗi nhóm phải xây dựng lại cùng một feature nhiều lần, các Data Engineer có thể tạo và công bố feature lên Catalog để các Data Scientist và ML Engineer dễ dàng tìm kiếm và tái sử dụng cho nhiều dự án khác nhau.

---

## 2. Những lợi ích nổi bật

| Lợi ích | Mô tả |
|---|---|
| **Tái sử dụng feature hiệu quả** | Các feature đã được xây dựng có thể được chia sẻ giữa nhiều nhóm và nhiều mô hình, giúp giảm công sức xử lý dữ liệu lặp lại. |
| **Quản lý tập trung** | Toàn bộ feature được lưu trữ và quản lý trong một hệ thống duy nhất, giúp dễ dàng theo dõi nguồn gốc, phiên bản và quyền truy cập. |
| **Đảm bảo tính nhất quán dữ liệu** | Những feature được sử dụng trong quá trình huấn luyện và đánh giá mô hình luôn có cùng định nghĩa, giảm nguy cơ sai lệch kết quả. |
| **Tăng tốc phát triển AI/ML** | Data Scientist có thể nhanh chóng tìm kiếm và sử dụng các feature sẵn có thay vì phải xây dựng lại từ đầu, rút ngắn đáng kể thời gian triển khai mô hình. |

---

## 3. Cơ chế hoạt động

Giải pháp sử dụng **Amazon S3 Tables** kết hợp với **Apache Iceberg** để lưu trữ dữ liệu feature. Nhờ đó hệ thống hỗ trợ:
- Quản lý phiên bản dữ liệu (versioning).
- Truy vấn dữ liệu tại các thời điểm trong quá khứ (time travel).
- Theo dõi nguồn gốc dữ liệu (data lineage).
- Chia sẻ feature giữa nhiều dự án và nhóm làm việc.

Các feature sau khi được tạo sẽ được đăng ký trong SageMaker Catalog, nơi người dùng có thể tìm kiếm, khám phá và yêu cầu quyền truy cập khi cần.

---

## 4. Ý nghĩa đối với doanh nghiệp

Việc xây dựng Offline Feature Store giúp doanh nghiệp chuẩn hóa quy trình quản lý dữ liệu Machine Learning, giảm sự trùng lặp trong quá trình phát triển, tăng khả năng cộng tác giữa các nhóm và đẩy nhanh tốc độ đưa các mô hình AI vào thực tế.

**Tóm lại:** SageMaker Unified Studio và SageMaker Catalog giúp tạo ra một kho lưu trữ feature tập trung, cho phép quản lý, chia sẻ và tái sử dụng dữ liệu hiệu quả hơn, từ đó nâng cao năng suất phát triển các dự án AI/ML trên AWS.

---

*Hình ảnh minh họa:*

![Blog 1 - Offline Feature Store](/images/Blog1.jpg)
