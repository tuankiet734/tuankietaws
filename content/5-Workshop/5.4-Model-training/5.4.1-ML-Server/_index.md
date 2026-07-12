---
title: "ML Training Server Provisioning"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.4.1. </b> "
---

### 5.4.1. Provisioning the ML Training Server (`ML-Forecast-Server`)

Model training requires a consistent environment, which is deployed as a dedicated virtual machine on **Amazon EC2**:

* **Instance Name Tag:** `ML-Forecast-Server`
* **Instance ID:** `i-019ac66f1b864b96a`
* **Instance Type:** `t2.micro`
* **Operating System:** Ubuntu Linux (64-bit x86)
* **Network Placement:** Launched in the public subnet of Availability Zone `ap-southeast-1b` (Singapore).
* **Security Group (`sg-0579af9926812195b` / `launch-wizard-3`):**
  * Permits Inbound SSH connections (port 22) from developer IPs for setup and debugging.
  * Permits Outbound connections on port `5432` to query feature tables in `training-db`.
  * Permits Outbound HTTPS traffic (port 443) to download required Python libraries.

##### Screenshot Guide:
* Open **Amazon EC2 Console** -> **Instances**. Take a screenshot showing details of the `ML-Forecast-Server` in the **Running** state.
* Save the screenshot in: `static/images/5-Workshop/5.4-Model-training/ec2-ml-server.png` and remove the comment markdown tags.

<!-- ![EC2 Server](/images/5-Workshop/5.4-Model-training/ec2-ml-server.png) -->
