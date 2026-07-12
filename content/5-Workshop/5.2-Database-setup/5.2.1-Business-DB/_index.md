---
title: "Business Database Provisioning"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.2.1. </b> "
---

### 5.2.1. Provisioning the Business Transaction Database (`fashion-rds`)

The primary database storing order transactions, stores, and product items is hosted on **Amazon RDS PostgreSQL** with the following configurations:

* **Engine Version:** PostgreSQL 15.18
* **Instance Class:** `db.t3.micro` (1 vCPU, 1 GiB RAM)
* **DB Instance Identifier:** `fashion-rds`
* **Master Username:** `dbadmin`
* **Allocated Storage:** 20 GiB (GP2 SSD, auto-scales up to 1000 GiB)
* **Database Name:** `fashiondb`
* **VPC:** `vpc-0426acd9a3039dbc2` (Default VPC)
* **Subnet Group:** `default-vpc-0426acd9a3039dbc2` covering all Availability Zones (`ap-southeast-1a`, `ap-southeast-1b`, `ap-southeast-1c`).

---

#### AWS Console Configuration Steps
1. Navigate to the **RDS** console.
2. Click **Create database**.
3. Choose **Standard create** and select the **PostgreSQL** engine.
4. Select **PostgreSQL 15.18-R1** or equivalent version.
5. Choose **Free Tier** templates and set DB Instance Identifier to `fashion-rds`.
6. Configure Master Username as `dbadmin` and enter your secure password.
7. Select the default VPC and enable **Publicly Accessible** options.
