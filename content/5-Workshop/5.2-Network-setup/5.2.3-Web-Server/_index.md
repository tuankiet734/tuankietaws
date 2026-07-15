---
title: "Launch EC2 Instance (Web Server)"
date: 2024-07-07
weight: 3
chapter: false
pre: " <b> 5.2.3. </b> "
---

### 5.2.3. Launch EC2 Instance (Web Server)

We will launch an EC2 instance to serve as the Web Application Server running the retail storefront application.

1. **Step 1:** Access the **EC2** service. In the **Instances** section, click **Launch an instance** to initialize a new virtual machine:
   * **Name and tags:** Enter `Web-Application-Server`.
   * **OS Image (AMI):** Select `Ubuntu`, version `Ubuntu Server 26.04 LTS (HVM)`, SSD Volume Type.
   
   ![Launch EC2 Instance](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231937.png)
2. **Step 2:** Configure the key pair and network settings for the server:
   * **Key pair:** Select your key pair to allow secure SSH connections.
   * **VPC:** Select the VPC hosting the system.
   * **Auto-assign public IP:** Select `Enable`.
   * **Firewall (security groups):** Select `Allow SSH traffic`, `Allow HTTPS traffic`, and `Allow HTTP traffic` to permit necessary inbound traffic.
   
   ![EC2 Key Pair and Network Settings](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231953.png)
3. **Step 3:** Click **Launch instance** to complete the process.
