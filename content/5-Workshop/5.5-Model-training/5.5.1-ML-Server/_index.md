---
title: "ML Training Server Provisioning"
date: 2024-07-07
weight: 1
chapter: false
pre : " <b> 5.5.1. </b> "
---

### 5.5.1. Provisioning the ML Training Server (`ML-Forecast-Server`)

Model training requires a consistent environment, which is deployed as a dedicated virtual machine on **Amazon EC2**:

* **Instance Name Tag:** `ML-Forecast-Server`
* **Instance ID:** `i-019ac66f1b864b96a`
* **Instance Type:** `t2.micro`
* **Operating System:** Ubuntu Linux (64-bit x86)
* **Network Placement:** Launched in the public subnet of Availability Zone `ap-southeast-1b` (Singapore).
* **Security Group (`sg-0579af9926812195b` / `launch-wizard-3`):**
  * **Inbound Rules:** Permits Inbound SSH connections (port 22) from developer IPs for setup and debugging.
  * **Outbound Rules:** 
    * Permits Outbound connections on port `5432` to query feature tables in `training-db` (or `fashion-rds`).
    * Permits Outbound HTTPS traffic (port 443) to download required Python libraries (`lightgbm`, `scikit-learn`, `psycopg2-binary`, etc.).

---

#### Step-by-Step Provisioning Guide on AWS Console:

1. **Access Service:** Sign in to the **AWS Console**, search for `EC2`, and navigate to the **EC2** dashboard.
2. **Launch Instance:** Click the **Launch instance** button.
3. **Configure Name & OS:**
   * **Name tag:** Enter `ML-Forecast-Server`.
   * **OS (AMI):** Select **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type** (64-bit x86).
4. **Instance Type & Key Pair:**
   * **Instance type:** Select `t2.micro` (or `t2.medium` for faster computation).
   * **Key pair:** Choose your existing key pair (`Thanh_key.pem` or `EC2.pem`) to enable secure SSH connection.
5. **Network Settings:**
   * **VPC:** Choose the Default VPC.
   * **Subnet:** Select any public subnet (e.g., Availability Zone `ap-southeast-1b`).
   * **Auto-assign public IP:** Select **Enable** to obtain a public IP.
   * **Security group:** Choose **Create security group**, name it `ml-server-sg`, and add Inbound/Outbound rules as described above.
6. **Storage:** Configure a **gp3** root volume with at least **15-20 GB** to fit all Python libraries and local model pickles.
7. **Launch:** Click **Launch instance** and wait for the instance state to transition to **Running**.

---

#### Verification on AWS Console:

![EC2 Server](/images/5-Workshop/5.5-Model-training/ec2-ml-server.png)

