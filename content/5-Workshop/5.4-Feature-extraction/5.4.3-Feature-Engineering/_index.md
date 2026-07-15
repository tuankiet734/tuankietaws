---
title: "Spark ETL Feature Engineering Script"
date: 2024-07-07
weight : 4
chapter: false
pre : " <b> 5.4.3. </b> "
---

### 5.4.3. Spark ETL Feature Engineering Script (`glue_feature_engineering.py`)

The core compute task is run via **Apache Spark** on **AWS Glue** to calculate historical time-series features across transactional lines.

---

#### Step-by-Step Spark Job Creation on AWS Console:

1. **Create New Job:** Navigate to AWS Glue -> **ETL jobs**, select **Spark script editor** and click **Create**.
2. **Configure Job Details:**
   * **Name:** Enter `glue_feature_engineering.py`.
   * **IAM Role:** Select `de-fashion-glue-role`.
   * **Language:** Select **Python or Spark**.
3. **Scale Settings:**
   * **Worker type:** Select **G.1X**.
   * **Number of workers:** Set to **20** (or configure lower according to your AWS account quotas).
4. **Load PostgreSQL JDBC Driver:**
   * Upload the JDBC jar file `postgresql-42.7.3.jar` to your S3 bucket.
   * In the job configurations page, navigate to **Job details** -> **Libraries** -> **Dependent jars path** and enter the S3 location (e.g., `s3://fashion-retail-model-storage/jars/postgresql-42.7.3.jar`).
5. **Input Spark SQL Code:** Copy the time-series engineering Spark script from [glue_feature_engineering.py](file:///d:/b%C3%A1o%20c%C3%A1o%20AWS/source_code/glue_feature_engineering.py) and paste it into the script editor.
6. **Save:** Click **Save**.

---

#### AWS Console Proof of Operation:

![AWS Glue Spark Feature Engineering Job](/images/5-Workshop/5.4-Feature-extraction/glue-lag-features.png)