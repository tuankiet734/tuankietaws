---
title: "Script Python trích xuất thô"
date: 2024-07-07
weight: 2
chapter: false
pre: " <b> 5.3.2. </b> "
---

### 5.3.2. Script Python Trích xuất dữ liệu thô (`de-fashion-rds-extract`)

Tác vụ đầu tiên chạy trên môi trường **Glue Python Shell** sử dụng thư viện `pandas` và `sqlalchemy` để truy vấn trực tiếp cơ sở dữ liệu Postgres nghiệp vụ và ghi file nén Parquet lên S3.

##### Toàn bộ mã nguồn script trích xuất:
```python
import sys
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from awsglue.utils import getResolvedOptions

# Đọc các tham số truyền vào từ cấu hình Glue Job
args = getResolvedOptions(sys.argv,
    ['db_host','db_port','db_name','db_user','db_pass','s3_bucket'])

# Tạo chuỗi kết nối engine PostgreSQL qua thư viện psycopg2
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
