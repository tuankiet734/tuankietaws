---
title: "Initialize Training Database"
date: 2024-07-07
weight : 3
chapter: false
pre : " <b> 5.3.2. </b> "
---

### 5.3.2. Initialize Training Database (`training-db`)

A dedicated training database is deployed independently to store the final processed features generated from the Spark ETL pipeline, feeding directly into the Machine Learning server:
* **Database Engine:** PostgreSQL 18.3
* **Instance Class:** `db.t3.micro` (1 vCPU, 1 GiB RAM)
* **DB Instance Identifier:** `training-db`
* **Master Username:** `dbadmin`
* **Allocated Storage:** 20 GiB (GP2 SSD)
* **Database Name:** `fashiondb`
* **VPC:** Default VPC (`vpc-0426acd9a3039dbc2`)
* **Actual Endpoint:** `training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com`

---

#### Step-by-Step Creation Guide on AWS Console:

1. **Access the Service:** Navigate to the **Amazon RDS Console**, click on **Databases** on the left menu.
2. **Create Database:** Click the orange **Create database** button.
3. **Choose Configuration:**
   * Select **Standard create** and select **PostgreSQL** as the Engine.
   * Under **Engine Version**, select **PostgreSQL 18.3** (the latest version to take advantage of performance enhancements for feature dataset handling).
4. **Select Template:** Select **Free Tier**.
5. **Configure Settings:**
   * **DB instance identifier:** Enter `training-db`.
   * **Master username:** Enter `dbadmin`.
   * **Master password:** Enter your secure password.
6. **Connectivity settings:**
   * Select the Default VPC.
   * **Public access:** Check **Yes** (to allow developer connections to verify feature calculations).
   * **VPC security group:** Select **Create new** and provide a distinct name.
7. **Additional Configuration:**
   * **Initial database name:** Enter `fashiondb`.
8. **Finalize:** Click **Create database** at the bottom and wait for the database creation to finish.

---

#### AWS Console Proof of Operation:

![Training RDS Database](/images/5-Workshop/5.3-Database-setup/training-db-detail.png)