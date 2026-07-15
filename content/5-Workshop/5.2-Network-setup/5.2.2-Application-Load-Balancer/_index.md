---
title: "Create Application Load Balancer (ALB)"
date: 2024-07-07
weight: 2
chapter: false
pre: " <b> 5.2.2. </b> "
---

### 5.2.2. Create Application Load Balancer (ALB)

We will configure two Application Load Balancers: an External ALB to receive traffic from the internet and an Internal ALB to route traffic internally within our private subnets.

#### 1. Configure External Application Load Balancer

1. **Step 1:** Access the **EC2** service. In the left navigation pane, scroll down to **Load Balancing** and select **Load balancers**. Click **Create load balancer**, and under the **Application Load Balancer** section, click **Create**.
   
   ![Create ALB](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231553.png)
2. **Step 2:** Configure the **Basic configuration** for External-ALB:
   * **Load balancer name:** Enter `External-ALB`.
   * **Scheme:** Select `Internet-facing` to receive traffic directly from the Internet.
   * **IP address type:** Select `IPv4`.
   
   ![External ALB Basic Config](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231724.png)
3. **Step 3:** Under **Network mapping**, map the Load Balancer to the Availability Zones (AZs) in your VPC:
   * **VPC:** Select the default VPC.
   * **Mappings:** Select at least two AZs (`us-east-1a` and `us-east-1b`) and their corresponding subnets to ensure high availability.
   
   ![External ALB Network Mapping](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231752.png)
4. **Step 4:** Create a Security Group for the Web Server (Click "Create security group" to configure in a new tab):
   * **Security group name:** Enter `my web`.
   * **Description:** Enter `Allows SSH access to developers`.
   * **VPC:** Select the VPC currently hosting the system.
   * **Outbound rules:** Select Type as `HTTP`, Port range as `80`, Destination as `Anywhere-IPv4` (`0.0.0.0/0`).
   * Click **Create security group** to finish.
   
   ![Create Security Group](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231809.png)
5. **Step 5:** Go back to the ALB creation tab, select the newly created Security Group (along with `my web`, `default`, `web-alb-sg`, `Web-Template`). In the **Listeners and routing** section:
   * **Protocol:** `HTTP`
   * **Port:** `80`
   * **Default action:** Select `Forward to target groups` and temporarily leave the Target Group field empty.
   
   ![External ALB Listeners and Security Groups](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231834.png)

#### 2. Configure Internal Application Load Balancer

1. **Step 1:** Click **Create load balancer** again and select **Application Load Balancer**. Under **Basic configuration**:
   * **Load balancer name:** Enter `Internal-ALB`.
   * **Scheme:** Select `Internal` (routes internal VPC traffic only).
   
   ![Internal ALB Basic Config](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231850.png)
2. **Step 2:** Under **Network mapping**, choose the same VPC and Availability Zones (`us-east-1a`, `us-east-1b`) as selected for the External ALB.
   
   ![Internal ALB Network Mapping](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231906.png)
3. **Step 3:** Under **Security groups**, select `default` and configure a listener on port `HTTP:80` to `Forward` to the corresponding internal Target Group.
   
   ![Internal ALB Listeners and Routing](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231923.png)
