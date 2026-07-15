---
title: "Glue & Lambda Cleanup"
date: 2024-07-07
weight: 4
chapter: false
pre : " <b> 5.9.4. </b> "
---

### 5.9.4. Deleting AWS Glue Jobs, Lambda Functions, and ECR Repositories

The final step is purging serverless compute resources, image repositories, and automation rules:

1. **AWS Glue:**
   * Open the **AWS Glue Studio** -> **ETL jobs**. Select and delete the `de-fashion-rds-extract` and `glue_feature_engineering.py` jobs.
   * Go to **Connections** in AWS Glue, select and delete any PostgreSQL database connection resources created for RDS.
2. **AWS Lambda:**
   * Open the **AWS Lambda Console** -> **Functions**.
   * Select your `FashionDemandForecastAPI` lambda function (and `DailyForecastTrigger` if applicable), click **Actions** -> Select **Delete**.
3. **Amazon ECR:**
   * Open the **Amazon ECR Console** -> **Repositories**.
   * Select the `fashion-demand-predictor` repository, click **Delete**, and type `delete` to confirm. This removes all stored Docker image layers and stops storage charges.
4. **Amazon EventBridge Scheduler:**
   * Open the **Amazon EventBridge Console** -> **Schedules** (or **Rules**).
   * Find your daily scheduler rule (e.g., `DailyForecastTriggerSchedule`), click **Delete** to deactivate automatic triggers.

---

{{% notice warning %}}
⚠️ **Warning:** Once RDS instances, S3 buckets, ECR repositories, and Lambda functions are deleted, all transaction history, precalculated feature tables, and serialized models are **permanently lost** and cannot be restored. Ensure you have copied all necessary performance metrics and logs before initiating cleanup.
{{% /notice %}}

