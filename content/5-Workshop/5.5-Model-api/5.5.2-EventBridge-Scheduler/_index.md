---
title: "Pipeline Automation"
date: 2024-07-07
weight: 2
chapter: false
pre: " <b> 5.5.2. </b> "
---

### 5.5.2. Pipeline Automation via Amazon EventBridge

To ensure the forecasting model is updated regularly as retail sales fluctuate daily, the entire ETL and training workflow is automated using an EventBridge scheduler rule.

##### Scheduler Orchestration Process:
1. An **Amazon EventBridge Rule** is defined to execute on a schedule (e.g. `cron(0 0 * * ? *)` running daily at midnight).
2. EventBridge triggers the Python Shell Glue job `de-fashion-rds-extract` to ingest the previous day's sales transactions.
3. Upon successful ingestion, a Glue trigger runs the PySpark job `glue_feature_engineering.py` to recalculate feature aggregates and write them to the `training-db` database.
4. An Amazon SNS notification notifies the `ML-Forecast-Server` instance to re-run the training script, generating and uploading a new model file to S3.

##### Screenshot Guide:
* Open **Amazon EventBridge Console** -> **Rules**. Locate your cron schedule rule and take a screenshot of its details page. 
* Save the screenshot in: `static/images/5-Workshop/5.5-Model-api/eventbridge-schedule.png` and remove the comment markdown tags.

<!-- ![EventBridge Rule](/images/5-Workshop/5.5-Model-api/eventbridge-schedule.png) -->
