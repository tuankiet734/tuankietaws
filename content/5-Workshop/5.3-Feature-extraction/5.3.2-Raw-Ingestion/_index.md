---
title: "Raw Data Ingestion Script"
date: 2024-07-07
weight: 2
chapter: false
pre: " <b> 5.3.2. </b> "
---

### 5.3.2. Raw Data Ingestion Script (`de-fashion-rds-extract`)

The initial data sync task runs on **AWS Glue Python Shell**, importing SQL datasets via `pandas` and `sqlalchemy` and saving Parquet outputs to Amazon S3.

##### Full Script Code:
```python
import sys
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from awsglue.utils import getResolvedOptions

# Resolve parameters passed to the Glue job
args = getResolvedOptions(sys.argv,
    ['db_host','db_port','db_name','db_user','db_pass','s3_bucket'])

# Create SQLAlchemy connection engine
engine = create_engine(
    f"postgresql+psycopg2://{args['db_user']}:{args['db_pass']}@"
    f"{args['db_host']}:{args['db_port']}/{args['db_name']}"
)

# Read database records into pandas DataFrames
transactions = pd.read_sql("SELECT * FROM transactions", engine)
products = pd.read_sql("SELECT * FROM products", engine)
stores = pd.read_sql("SELECT * FROM stores", engine)

# Calculate S3 target folders by execution date
today = datetime.now().strftime("%Y-%m-%d")
base = f"s3://{args['s3_bucket']}/landing_zone/{today}"

# Export datasets as compressed Parquet files
transactions.to_parquet(f"{base}/transactions.parquet", index=False)
products.to_parquet(f"{base}/products.parquet", index=False)
stores.to_parquet(f"{base}/stores.parquet", index=False)

print("Extract thanh cong!")
```
