---
title: "Security and Network Configuration"
date: 2024-07-07
weight: 3
chapter: false
pre: " <b> 5.2.3. </b> "
---

### 5.2.3. Security and Network Configurations

Both PostgreSQL instances are configured to allow secure interactions between compute resources (AWS Glue, EC2, Lambda) while preventing unauthorized public ingress.

* **Publicly Accessible:** Set to `True` to allow direct access from external developer workstations.
* **Security Group (`sg-0fecd1d2df90f2a69`):**
  * **Inbound Rules:**
    * Port `5432` / Protocol TCP: Allows connections from your local developer IP address (for DBeaver/pgAdmin client querying).
    * Port `5432` / Protocol TCP: Allows traffic originating from the `ML-Forecast-Server` security group (`sg-0579af9926812195b`).
    * Port `5432` / Protocol TCP: A self-referencing rule allowing security group members to talk to each other. This is required for AWS Glue JDBC connections.
  * **Outbound Rules:** Allows all traffic outbound (Default).
* **Storage Encryption:** Enabled and encrypted at rest using the default **AWS KMS** key (`fe12be50-a2cf-44d1-a1da-3ce27e40686d`).

##### Screenshot Guide:
* Open **AWS Management Console** -> **RDS** -> **Databases**. Capture a screenshot of the database lists showing both database endpoints in the **Available** state.
* Save the screenshot in the project directory at: `static/images/5-Workshop/5.2-Database-setup/rds-console.png` and remove the comment markdown notation.

<!-- ![RDS Console](/images/5-Workshop/5.2-Database-setup/rds-console.png) -->
