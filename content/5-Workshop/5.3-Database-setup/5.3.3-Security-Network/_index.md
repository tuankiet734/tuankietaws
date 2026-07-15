---
title: "Configure Network and Security"
date: 2024-07-07
weight: 3
chapter: false
pre : " <b> 5.3.3. </b> "
---

### 5.3.3. Configure Network and Security (Security & Network Groups)

To ensure robust data protection while enabling necessary integration points, network routing and security are configured via **VPC Security Group** rules:

* **Storage Encryption:** Enabled for both databases using the default **AWS KMS** key (`fe12be50-a2cf-44d1-a1da-3ce27e40686d`).
* **Active Security Group:** `sg-0fecd1d2df90f2a69`

---

#### Step-by-Step Security Group Inbound Rules Configuration:

1. **Navigate to EC2:** Open the AWS Console and search for **EC2**.
2. **Select Security Groups:** Click on **Security Groups** under the **Network & Security** section on the left navigation panel.
3. **Select Security Group:** Select the security group attached to the RDS databases (e.g., `sg-0fecd1d2df90f2a69`).
4. **Edit Inbound Rules:** Click the **Inbound rules** tab and click the **Edit inbound rules** button.
5. **Configure 3 Mandatory Rules:**
   * **Rule 1 (Developer Access):** 
     * **Type:** Select `PostgreSQL` (port `5432`).
     * **Source:** Select **My IP** (automatically detects your local IP). This allows local clients (DBeaver, pgAdmin) to query the databases.
   * **Rule 2 (EC2 Training Server Access):**
     * **Type:** Select `PostgreSQL` (port `5432`).
     * **Source:** Select **Custom** and enter the Security Group ID of the `ML-Forecast-Server` (`sg-0579af9926812195b`).
   * **Rule 3 (AWS Glue Connection Self-Reference):**
     * **Type:** Select `PostgreSQL` (port `5432`).
     * **Source:** Select **Custom** and enter this Security Group's own ID (`sg-0fecd1d2df90f2a69` - Self-referencing rule).
6. **Save Configurations:** Click **Save rules** to apply the inbound routing.

---

#### AWS Console Proof of Operation:

Below is the screenshot showing the Inbound Rules configuration of the Security Group on the AWS Console:

![Security Group Inbound Rules](/images/5-Workshop/5.3-Database-setup/security-group-inbound-rules.png)