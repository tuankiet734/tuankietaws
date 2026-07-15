---
title: "Verify Connections"
date: 2024-07-07
weight: 4
chapter: false
pre : " <b> 5.3.4. </b> "
---

### 5.3.4. Database Connection Verification and Table Setup

Once the RDS instances are available and security groups are configured, we verify connection access and initialize the baseline table schemas.

---

#### Step 1: Verify Connections via CLI (`psql`)

Run the following psql connection commands from your terminal to verify open network pathing:

##### Connect to Central DB (Business Database):
```bash
psql -h fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com -p 5432 -U dbadmin -d fashiondb
```

##### Connect to Training DB (Feature Store Database):
```bash
psql -h training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com -p 5432 -U dbadmin -d fashiondb
```
*(Enter your password when prompted to establish session access)*

---

#### Step 2: Initialize Table Schemas on Central DB (`fashion-rds`)

Upon successful connection (via pgAdmin, DBeaver, or psql CLI), execute the following DDL script on `fashion-rds` to prepare the core tables:

```sql
-- 1. Products table
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2)
);

-- 2. Stores table
CREATE TABLE stores (
    store_id VARCHAR(50) PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(50)
);

-- 3. Historical transactions table
CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    store_id VARCHAR(50) REFERENCES stores(store_id),
    product_id VARCHAR(50) REFERENCES products(product_id),
    date DATE,
    qty INT
);
```

These baseline tables will be extracted by AWS Glue daily to compile time-series features.

---

#### AWS Console Proof of Operation:
Below is the screenshot showing the connection verification via DBeaver:

![DBeaver Connections](/images/5-Workshop/5.3-Database-setup/dbeaver-connections.png)