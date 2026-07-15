---
title: "Create CloudFront Distribution"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.2.1. </b> "
---

### 5.2.1. Create CloudFront Distribution

In this section, we will create a CloudFront Distribution to distribute content from API Gateway in an optimized and secure manner.

1. **Step 1:** Access the AWS Management Console, search for "cloudfront" in the search bar, and select the **CloudFront** service.
   
   ![CloudFront Search](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20230833.png)
2. **Step 2:** On the CloudFront Distributions dashboard, click **Create distribution**. In the **Step 1: Choose a plan** section, select the Free package ($0/month) and click **Next**.
   
   ![Choose Plan](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20230959.png)
3. **Step 3:** Under **Step 2: Get started**, configure the following parameters:
   * **Distribution name:** Enter `WebApp-Distribution`.
   * **Distribution type:** Select `Single website or app`.
   * Click **Next** to continue.
   
   ![Get Started](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231043.png)
4. **Step 4:** Under **Step 3: Specify origin**, configure the API Gateway endpoint as the data source (Origin):
   * **Origin type:** Select `API Gateway`.
   * **API Gateway origin:** Enter your API endpoint address (e.g., `5e0wzdirtc.execute-api.ap-southeast-1.amazonaws.com`).
   * Click **Next** to continue.
   
   ![Specify Origin](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231122.png)
5. **Step 5:** Under **Step 4: Enable security**, enable the Web Application Firewall (WAF) to protect the application from common web attacks:
   * Choose default protection rules or Rate limiting to prevent Denial of Service (DDoS) attacks.
   * Click **Next**.
   
   ![Enable Security](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231241.png)
6. **Step 6:** Under **Step 5: Review and create**, review all configured settings (Origin, Cache settings, Security) and click **Create distribution**.
   
   ![Review and Create](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231320.png)
7. **Step 7:** Once completed, you will be redirected to the Distributions list page. Wait until the **Status** column displays **Enabled**.
   
   ![CloudFront Status Enabled](/images/5-Workshop/5.2-Network-setup/Screenshot%202026-07-14%20231521.png)
