---
title: "ETL Architecture Overview"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.3.1. </b> "
---

### 5.3.1. ETL Architecture Overview

The data pipeline prepared for machine learning modeling runs in two sequential phases:

{{<mermaid>}}
graph TD
    RDS[Central RDS] -->|1. Extract| PythonJob[de-fashion-rds-extract]
    PythonJob -->|Save as Parquet| S3Landing[S3 Landing Zone]
    S3Landing -->|2. Ingest| SparkJob[glue_feature_engineering.py]
    SparkJob -->|Compute Lags, Rolling, Velocity| ProcessedFeatures[Feature Calculations]
    ProcessedFeatures -->|3. Parallel Writes| CentralDB[Central RDS]
    ProcessedFeatures -->|3. Parallel Writes| TrainingDB[Training RDS]
{{</mermaid>}}

#### Detailed Operations:
1. **Raw Data Extraction (Extract):** A Python Shell job queries the `fashion-rds` central database, fetches raw transactions, products, and stores tables, and dumps them as compressed Parquet files to an S3 staging area.
2. **Feature Engineering (Transform):** A PySpark job reads raw files from S3, cleans values (calculating median prices for categories, missing colors), and uses **Window Functions** to build time-series analytics (lagged sales, moving averages, sales velocity).
3. **Data Load (Load):** Persists the finished dataset parallelly back to both PostgreSQL databases.
