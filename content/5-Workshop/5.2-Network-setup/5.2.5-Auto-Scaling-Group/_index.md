---
title: "Configure Auto Scaling Group (ASG)"
date: 2024-07-07
weight: 5
chapter: false
pre: " <b> 5.2.5. </b> "
---

### 5.2.5. Configure Auto Scaling Group (ASG)

We will configure an Auto Scaling Group to automatically scale the number of Web Server instances based on traffic demand.

1. **Step 1:** In the EC2 console, select **Auto Scaling groups** and click **Create Auto Scaling group**:
   * **Auto Scaling group name:** Enter `WebApp-ASG`.
   * **Launch template:** Select the appropriate pre-configured launch template.
   * Click **Next**.
   
   ![Create ASG](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232039.png)
2. **Step 2:** Under **Step 2: Choose instance launch options**, configure hardware requirements for instance scaling:
   * Set vCPUs from 1 to 5, and Memory (RAM) from 1 to 5 GiB.
   
   ![ASG Launch Options](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232110.png)
3. **Step 3:** Select the VPC and map the network zones:
   * **Availability Zones and subnets:** Select at least `us-east-1a` and `us-east-1b`.
   * **Availability Zone distribution:** Select `Balanced best effort`.
   * Click **Next**.
   
   ![ASG Network Mappings](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232127.png)
4. **Step 4:** Under **Step 3: Integrate with other services**, bind the Auto Scaling Group with the Load Balancer:
   * **Load balancing:** Select `Attach to an existing load balancer`.
   * Select `Choose from your load balancer target groups`.
   * **Existing load balancer target groups:** Select the Target Group created in step 4 (e.g., `Internal-Backend-TG`).
   * Click **Next**.
   
   ![ASG ALB Integration](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232157.png)
5. **Step 5:** Under **Step 4: Configure group size and scaling**, configure instance limits:
   * **Desired capacity:** Enter `1`.
   * **Min desired capacity:** Enter `1`.
   * **Max desired capacity:** Enter `5`.
   * **Automatic scaling:** Select `No scaling policies`.
   * Click **Next**.
   
   ![ASG Group Size and Scaling](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232212.png)
6. **Step 6:** Under **Step 5: Add notifications**, click **Next** to skip SNS notifications (or set up notifications if you want to monitor scaling events).
   
   ![ASG Notifications](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232230.png)
7. **Step 7:** Under **Step 7: Review**, review all configured Auto Scaling Group settings and click **Create Auto Scaling group** to activate.
   
   ![ASG Review and Create](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20232245.png)
