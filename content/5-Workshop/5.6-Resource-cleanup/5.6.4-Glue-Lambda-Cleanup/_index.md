---
title: "Glue & Lambda Cleanup"
date: 2024-07-07
weight: 4
chapter: false
pre: " <b> 5.6.4. </b> "
---

### 5.6.4. Deleting AWS Glue Jobs and Lambda Functions

1. Open **AWS Glue Studio** -> **ETL jobs**, select and delete `de-fashion-rds-extract` and `glue_feature_engineering.py`.
2. Open the **AWS Lambda Console** and delete your Model API lambda function.
3. Open **Amazon EventBridge** -> **Rules** and delete the daily schedule rule.

---

{{% notice warning %}}
⚠️ **Warning:** Once RDS instances and S3 buckets are deleted, all transaction history and model files are **permanently lost** and cannot be restored. Ensure you have copied all necessary performance metrics and logs before initiating cleanup.
{{% /notice %}}
