---
title: "Initialize Business Database"
date: 2024-07-07
weight: 1
chapter: false
pre : " <b> 5.3.1. </b> "
---

### 5.3.1. Initialize Business Database (`fashion-rds`)

The central database storing sales orders, transactions, products, and store data is deployed on **Amazon RDS PostgreSQL** with the following detailed parameters:
* **Database Engine:** PostgreSQL 15.18
* **Instance Class:** `db.t3.micro` (1 vCPU, 1 GiB RAM)
* **DB Instance Identifier:** `fashion-rds`
* **Master Username:** `dbadmin`
* **Allocated Storage:** 20 GiB (GP2 SSD, Auto-scaling enabled)
* **Database Name:** `fashiondb`
* **VPC:** Default VPC (`vpc-0426acd9a3039dbc2`)
* **Actual Endpoint:** `fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com`

---

#### Step-by-Step Creation Guide on AWS Console:

1. **Access the Service:** Sign in to the **AWS Management Console**, search for `RDS` in the top search bar, and select **RDS**.
2. **Create Database:** On the RDS Dashboard, click the orange **Create database** button.
3. **Choose Creation Method:** Select **Standard create** to customize configuration details.
4. **Select Engine Options:** 
   * Select **PostgreSQL** as the Engine type.
   * Under **Engine Version**, select **PostgreSQL 15.18-R1** from the dropdown list.
5. **Select Template:** Select **Free Tier** to run within the free tier budget limits (automatically sets class to `db.t3.micro` and storage to 20 GiB).
6. **Configure Settings:**
   * **DB instance identifier:** Enter `fashion-rds`.
   * **Credentials specification:** 
     * **Master username:** Enter `dbadmin`.
     * **Master password:** Enter your secure database password.
7. **Instance & Storage Configuration:** Keep the default `db.t3.micro` class and **gp2** storage type with **20 GiB** capacity. Keep **Enable storage autoscaling** checked.
8. **Configure Connectivity:**
   * **Virtual Private Cloud (VPC):** Select the Default VPC.
   * **Public access:** Check **Yes** (to allow direct querying from client tools like DBeaver/pgAdmin).
   * **VPC security group:** Select **Create new** and provide a name for the security group.
9. **Additional Configuration:** Click to expand this section at the bottom of the page:
   * **Initial database name:** Enter `fashiondb`.
   * Keep the default Backup and Encryption settings.
10. **Finalize:** Click **Create database** at the bottom. It will take 5-7 minutes for the RDS instance to transition to the **Available** state.

---

#### AWS Console Proof of Operation:

![Central RDS Database](/images/5-Workshop/5.3-Database-setup/rds-all-databases.png)