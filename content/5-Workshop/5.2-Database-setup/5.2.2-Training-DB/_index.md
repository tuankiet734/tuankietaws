---
title: "Training Database Provisioning"
date: 2024-07-07
weight: 2
chapter: false
pre: " <b> 5.2.2. </b> "
---

### 5.2.2. Provisioning the Training Database (`training-db`)

The dedicated feature store database used to hold aggregated dataset features is launched as a separate instance:

* **Engine Version:** PostgreSQL 18.3 (A newer major engine to support advanced analytics)
* **Instance Class:** `db.t3.micro`
* **DB Instance Identifier:** `training-db`
* **Master Username:** `dbadmin`
* **Allocated Storage:** 20 GiB (GP2 SSD)
* **Database Name:** `fashiondb`
* **VPC:** `vpc-0426acd9a3039dbc2`

---

#### AWS Console Configuration Steps
1. On the **Amazon RDS** console, click **Create database**.
2. Select **Standard create** and the **PostgreSQL** engine.
3. Select version **PostgreSQL 18.3**.
4. Choose **Free Tier** templates and set DB Instance Identifier to `training-db`.
5. Set Master Username to `dbadmin` and enter your password.
6. Match the VPC network configurations with the central database to ensure easy internal routing.
