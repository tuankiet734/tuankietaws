---
title : "Architecture Overview"
date : 2024-07-07
weight : 1
chapter : false
pre : " <b> 5.1. </b> "
---

#### System Architecture Diagram

Below is the network infrastructure and machine learning pipeline architecture deployed on **Amazon Web Services (AWS)**:

![overview](/images/5-Workshop/5.1-Workshop-overview/diagram1.png)

#### System Components

The system is divided into two primary zones: **Web Application & APIs** (for user access) and **Machine Learning Pipeline** (for data processing and forecasting).

##### 1. Web Application & API Group (User Access Layer)
* **AWS CloudFront:** Serves as a Content Delivery Network (CDN) to optimize page load speeds by caching static assets like CSS, JS, and product images.
* **External Application Load Balancer (ALB):** Receives client HTTP/HTTPS requests and distributes traffic across the Web Application layer.
* **Web Application (Auto Scaling Group):** Contains EC2 instances running the retail web storefront (e.g. `Web-Application-Server`), auto-scaling dynamically with user traffic.
* **Internal ALB:** Securely routes API calls from the Web Application to private backend APIs.
* **RESTful API (Auto Scaling Group):** Contains EC2 instances running backend services (e.g. `fashion-api-server`), handling checkout, carts, and user profiles.

##### 2. Data & Machine Learning Pipeline Group
* **Central Database (`fashion-rds`):** Amazon RDS PostgreSQL database storing transactional application data (orders, users, inventory).
* **Feature Extraction (AWS Glue):** Serverless Spark service performing ETL jobs (`de-fashion-rds-extract` and `glue_feature_engineering.py`) to process raw database records.
* **Training Database (`training-db`):** Amazon RDS PostgreSQL database storing cleaned feature tables prepared for ML model ingestion.
* **Training Model (ML-Forecast-Server):** Dedicated EC2 machine (`ML-Forecast-Server`) loading features from `training-db` and executing training models.
* **Model Storage (Amazon S3):** Stores trained model artifacts inside the `fashion-retail-model-storage` S3 bucket.
* **Model API (AWS Lambda):** Serverless function loading artifacts from S3 and exposing endpoints to serve real-time predictions.
* **Daily Schedule (Amazon EventBridge):** Triggers daily automated pipeline execution to extract new features and update models.