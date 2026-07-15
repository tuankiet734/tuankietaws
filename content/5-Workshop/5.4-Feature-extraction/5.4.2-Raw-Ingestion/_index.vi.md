---
title: "Script Python trích xuất thô"
date: 2024-07-07
weight: 2
chapter: false
pre : " <b> 5.4.2. </b> "
---

### 5.4.2. Script Python Trích xuất dữ liệu thô (`de-fashion-rds-extract`)

Tác vụ đầu tiên chạy trên môi trường **AWS Glue Python Shell** để truy vấn trực tiếp cơ sở dữ liệu PostgreSQL nghiệp vụ và kết xuất file nén Parquet lên vùng đệm Landing Zone trên S3.

---

#### Hướng dẫn tạo Glue Job trên AWS Console:

1. **Mở AWS Glue Console:** Truy cập dịch vụ **AWS Glue** trên AWS Console.
2. **Tạo Job:** Ở danh sách menu bên trái, nhấp vào **ETL jobs** (trong mục **Data Integration and ETL**), sau đó chọn **Spark script editor** hoặc **Python Shell script editor** (chọn **Python Shell**).
3. **Cấu hình Job Details:**
   * **Name:** Đặt tên job là `de-fashion-rds-extract`.
   * **IAM Role:** Chọn role `de-fashion-glue-role` (đã được cấp quyền truy cập S3 và VPC).
   * **Python version:** Chọn `Python 3.9` hoặc phiên bản mới hơn.
4. **Nhập Mã nguồn:** Sao chép toàn bộ mã nguồn bên dưới và dán vào trình biên tập code trực tuyến của Glue:

```python
import sys
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from awsglue.utils import getResolvedOptions

# Đọc các tham số truyền vào từ cấu hình Glue Job
args = getResolvedOptions(sys.argv,
    ['db_host','db_port','db_name','db_user','db_pass','s3_bucket'])

# Tạo chuỗi kết nối engine PostgreSQL qua thư viện sqlalchemy
engine = create_engine(
    f"postgresql+psycopg2://{args['db_user']}:{args['db_pass']}@"
    f"{args['db_host']}:{args['db_port']}/{args['db_name']}"
)

# Truy vấn dữ liệu thô từ 3 bảng nghiệp vụ chính
transactions = pd.read_sql("SELECT * FROM transactions", engine)
products = pd.read_sql("SELECT * FROM products", engine)
stores = pd.read_sql("SELECT * FROM stores", engine)

# Xác định thư mục đích trên S3 theo ngày hiện tại
today = datetime.now().strftime("%Y-%m-%d")
base = f"s3://{args['s3_bucket']}/landing_zone/{today}"

# Xuất dữ liệu ra file nén Parquet tốc độ cao
transactions.to_parquet(f"{base}/transactions.parquet", index=False)
products.to_parquet(f"{base}/products.parquet", index=False)
stores.to_parquet(f"{base}/stores.parquet", index=False)

print("Extract thanh cong!")
```

5. **Cấu hình tham số chạy (Job parameters):** Cuộn xuống phần **Advanced properties** -> **Job parameters** và thêm các cặp Key/Value cụ thể của bạn:
   * `--db_host`: `fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com`
   * `--db_port`: `5432`
   * `--db_name`: `fashiondb`
   * `--db_user`: `dbadmin`
   * `--db_pass`: *(Mật khẩu database của bạn)*
   * `--s3_bucket`: `fashion-retail-model-storage`
6. **Lưu Job:** Nhấp nút **Save** ở góc trên cùng bên phải.

---

#### Minh chứng thực tế trên AWS Console:

![AWS Glue Ingestion Job](/images/5-Workshop/5.4-Feature-extraction/glue-jdbc-config.png)