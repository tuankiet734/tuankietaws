---
title: "Script Spark ETL kỹ nghệ đặc trưng"
date: 2024-07-07
weight : 4
chapter: false
pre : " <b> 5.4.3. </b> "
---

### 5.4.3. Script Spark ETL Kỹ nghệ Đặc trưng (`glue_feature_engineering.py`)

Tác vụ chính được thực hiện bằng **Apache Spark** trên **AWS Glue** để tính toán các đặc trưng chuỗi thời gian cho điểm dữ liệu.

---

#### Hướng dẫn cấu hình Spark Job trên AWS Console:

1. **Tạo Job mới:** Truy cập AWS Glue -> **ETL jobs**, chọn **Spark script editor** và nhấp **Create**.
2. **Cấu hình Job Details:**
   * **Name:** Đặt tên job là `glue_feature_engineering.py`.
   * **IAM Role:** Chọn role `de-fashion-glue-role`.
   * **Language:** Chọn **Python or Spark**.
3. **Cấu hình Hiệu năng (Scale Options):**
   * **Worker type:** Chọn **G.1X**.
   * **Number of workers:** Nhập **20** (hoặc cấu hình thấp hơn tuỳ hạn mức AWS của bạn).
4. **Nạp Driver PostgreSQL:** 
   * Tải driver JDBC PostgreSQL `postgresql-42.7.3.jar` lên thư mục S3 của bạn.
   * Tại tab **Job details** -> **Libraries** -> **Dependent jars path**, nhập đường dẫn dẫn tới file jar đó (ví dụ: `s3://fashion-retail-model-storage/jars/postgresql-42.7.3.jar`).
5. **Nhập Mã nguồn Spark SQL:** Sao chép đoạn code tính toán Lags, Rolling, Velocity trong file [glue_feature_engineering.py](file:///d:/b%C3%A1o%20c%C3%A1o%20AWS/source_code/glue_feature_engineering.py) dán vào phần soạn thảo script của Glue Job.
6. **Lưu Job:** Nhấp nút **Save**.

---

#### Minh chứng thực tế trên AWS Console:

![AWS Glue Spark Feature Engineering Job](/images/5-Workshop/5.4-Feature-extraction/glue-lag-features.png)