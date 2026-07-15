---
title: "Python Raw Extraction Script"
date: 2024-07-07
weight: 2
chapter: false
pre : " <b> 5.4.2. </b> "
---

### 5.4.2. Python Raw Extraction Script (`de-fashion-rds-extract`)

The initial extraction task is deployed on **AWS Glue Python Shell** to query PostgreSQL tables and save the data in compressed Parquet files to the S3 Landing Zone.

---

#### Step-by-Step Glue Job Creation on AWS Console:

1. **Open AWS Glue:** Search for **AWS Glue** in the AWS Console.
2. **Create Job:** Under **Data Integration and ETL** on the left menu, select **ETL jobs**. Choose **Python Shell script editor** and click **Create**.
3. **Configure Job Details:**
   * **Name:** Enter `de-fashion-rds-extract`.
   * **IAM Role:** Select `de-fashion-glue-role` (with VPC and S3 read/write permissions).
   * **Python version:** Select `Python 3.9` or latest.
4. **Input Source Code:** Paste the following code into the online script editor pane:

```python
import sys
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from awsglue.utils import getResolvedOptions

# Retrieve job parameters
args = getResolvedOptions(sys.argv,
    ['db_host','db_port','db_name','db_user','db_pass','s3_bucket'])

# Create PostgreSQL database engine connection via sqlalchemy
engine = create_engine(
    f"postgresql+psycopg2://{args['db_user']}:{args['db_pass']}@"
    f"{args['db_host']}:{args['db_port']}/{args['db_name']}"
)

# Query business tables
transactions = pd.read_sql("SELECT * FROM transactions", engine)
products = pd.read_sql("SELECT * FROM products", engine)
stores = pd.read_sql("SELECT * FROM stores", engine)

# Define destination S3 path prefixed by today's date
today = datetime.now().strftime("%Y-%m-%d")
base = f"s3://{args['s3_bucket']}/landing_zone/{today}"

# Output as compressed Parquet files
transactions.to_parquet(f"{base}/transactions.parquet", index=False)
products.to_parquet(f"{base}/products.parquet", index=False)
stores.to_parquet(f"{base}/stores.parquet", index=False)

print("Extract thanh cong!")
```

5. **Configure Run Parameters (Job parameters):** Expand **Advanced properties** -> **Job parameters** and add the following keys and values:
   * `--db_host`: `fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com`
   * `--db_port`: `5432`
   * `--db_name`: `fashiondb`
   * `--db_user`: `dbadmin`
   * `--db_pass`: *(Your database password)*
   * `--s3_bucket`: `fashion-retail-model-storage`
6. **Save:** Click **Save** in the top-right corner.

---

#### AWS Console Proof of Operation:

![AWS Glue Ingestion Job](/images/5-Workshop/5.4-Feature-extraction/glue-jdbc-config.png)