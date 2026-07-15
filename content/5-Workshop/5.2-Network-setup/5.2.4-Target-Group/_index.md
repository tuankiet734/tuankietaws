---
title: "Configure Target Group"
date: 2024-07-07
weight: 4
chapter: false
pre: " <b> 5.2.4. </b> "
---

### 5.2.4. Configure Target Group

We will configure the Target Group to route incoming requests from the Load Balancer to the appropriate EC2 server instances.

1. **Step 1:** In the **Load Balancing** section of the EC2 service dashboard, click **Target groups**. Click **Create target group**:
   * **Target type:** Select `Instances`.
   * **Target group name:** Enter `Internal-Backend-TG`.
   * **Protocol:** `HTTP`, **Port:** `80`.
   * Click **Next** to proceed to the next step.
   
   ![Create Target Group](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232007.png)
2. **Step 2:** Register servers (Targets) to the group:
   * Select the target EC2 servers from the list (for example, `my web server` with ID `i-0158bbf025496e997`).
   * Input the service port (**Port:** `80`) and click **Include as pending below**.
   * Review the list under **Review targets** and click **Create target group**.
   
   ![Register Targets](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232022.png)
