---
title: "Day 1"
date: 2026-06-01
weight: 1
chapter: false
pre: " <b> 1.1. </b> "
---

# Work Log: Account Setup, AWS Credits, and Core Guided Labs

> **Day 1 - Monday, June 01, 2026:** Activated the AWS student account, requested initial credits, and successfully completed 5 foundational console tasks to secure additional promotional credits.

---

### Objectives for the Day

- Register and configure a new AWS account, obtaining **$100 in initial credits** from the program.
- Complete **5 practical tasks** on the AWS Console to earn an extra **$100 credit** ($20 per task).
- gain initial familiarity with 5 foundational AWS services: EC2, Bedrock, Budgets, Lambda, and RDS.
- Understand the basics of AWS billing controls, security configurations, and resource cleanup.

---

### Task 1: Launch an EC2 Virtual Machine (+$20 Credit)

**Objective:** Provision and manage a Linux-based Virtual Machine in the cloud.

**Service Overview:** **Amazon EC2 (Elastic Compute Cloud)** provides resizable virtual computing capacity, enabling users to launch virtual servers with customized operating systems and networking.

**Steps Executed:**
1. Navigate to the **AWS Console** → locate the **Explore AWS** home page widget → select the **Launch an instance using EC2** task.
2. Select **Start activity** to initiate the guided lab.
3. Configure the VM:
   - Name tag: `FCA-Test-Server`
   - OS Image (AMI): Standard Amazon Linux 2023 (Free Tier eligible).
   - Instance Type: Keep default micro configuration (`t3.micro` or `t2.micro`).
4. Generate a new cryptographic Key Pair for secure access:
   - Key pair name: `fca-keypair`
   - Key pair type: **RSA**
   - Private key file format: **.pem** (saved locally).
5. Establish a Security Group with default rules allowing essential traffic.
6. Verify configurations and select **Launch Instance**.
7. **Verification Step:** Check the instance dashboard to confirm the instance status transitions to **Running** and passes the **2/2 status checks**.
8. **Teardown (Crucial):** Select the instance → Instance State → **Terminate Instance** to stop resource consumption.

> **Key Lesson:** Launching resources on AWS takes only a few clicks, but they incur ongoing charges. Terminating the EC2 instance immediately after testing is vital to prevent credit drain. Always check that the associated EBS volume is also deleted.

---

### Task 2: Prompting in Amazon Bedrock Playground (+$20 Credit)

**Objective:** Explore generative AI capabilities using foundational language models on AWS.

**Service Overview:** **Amazon Bedrock** is a fully managed service that offers access to high-performing foundation models from leading AI companies (such as Anthropic, Meta, Cohere) via a single API, without managing server infrastructure.

**Steps Executed:**
1. Open the **Amazon Bedrock Console** → choose the task **Use a foundation model in Amazon Bedrock**.
2. Request model access for **Claude 3 Haiku** (a fast, cost-efficient model for general text tasks).
3. If an access authorization error occurs, submit a brief justification under **Model access** to request permission.
4. Once access is active, navigate to the **Text Playground** and select **Claude 3 Haiku**.
5. Input a prompt (e.g., "Summarize the benefits of cloud computing in three bullet points") and click **Run**.
6. Review the output, adjust parameters like Temperature (to control creativity), and click **Finish** to complete the task.

> **Key Lesson:** Access to advanced AI models is governed by AWS's Responsible AI policies. Submitting a clear, professional use case description accelerates the allowlisting process.

---

### Task 3: Configure Cost Alerting in AWS Budgets (+$20 Credit)

**Objective:** Set up proactive alerts to monitor credit usage and prevent billing surprises.

**Service Overview:** **AWS Budgets** tracks resource spending and sends alerts via email or SNS when costs approach or exceed defined thresholds.

**Steps Executed:**
1. Access the **AWS Billing Console** → select **Budgets** → start the task **Set up a cost budget using AWS Budgets**.
2. Click **Start activity** to launch the creation wizard.
3. Configure budget settings:
   - Budget Type: Cost Budget.
   - Period: Monthly.
   - Budgeted Amount: $20.00.
4. Define alert thresholds:
   - Set an alert when actual costs reach **80% ($16.00)** of the budget.
   - Enter a personal email address to receive notifications.
5. Review configurations and click **Create budget**.

> **Key Lesson:** Setting up a budget is the first line of defense in any cloud project. Proactive notifications ensure that runaway resources are identified before they consume all available credits.

---

### Task 4: Deploy a Serverless Web Application with AWS Lambda (+$20 Credit)

**Objective:** Run backend code using a serverless architecture.

**Service Overview:** **AWS Lambda** executes code in response to events (like HTTP requests) and automatically manages the underlying compute resource scaling. Charges are based solely on execution time, meaning zero costs when inactive.

**Steps Executed:**
1. Navigate to the **AWS Lambda Console** → select the task **Create a web app using AWS Lambda**.
2. Click **Start activity** → select **Use a blueprint** → search for the template **Getting started with Lambda HTTP**.
3. Configure the function:
   - Function name: `fca-http-lambda-app`
   - Select the acknowledgment box for creating an IAM role with basic permissions.
4. Click **Create function** and wait for deployment.
5. **Testing Step:** Copy the generated **Function URL** from the dashboard, paste it into a browser tab, and verify that it returns a successful JSON greeting.
6. **Teardown:** Delete the function to clean up the workspace.

> **Key Lesson:** Serverless computing eliminates the overhead of server patching and scaling. It scales down to zero, ensuring that a deployed function that receives no traffic costs nothing.

---

### Task 5: Launch a Managed Relational Database using RDS (+$20 Credit)

**Objective:** Deploy a secure, managed relational database cluster.

**Service Overview:** **Amazon RDS (Relational Database Service)** automates complex database administration tasks, including database provisioning, patching, backups, and scaling.

**Steps Executed:**
1. Open the **Amazon RDS Console** → choose the task **Create an Amazon RDS Database**.
2. Select **Easy create** to use optimized defaults.
3. Configuration parameters:
   - Database Engine: **Aurora (PostgreSQL Compatible)**.
   - DB Instance Class: Select the smallest available instance type.
4. Click **Create database** and monitor the database status until it shifts to **Available**.
5. **Teardown Step (Order Matters):**
   - Attempting to delete the cluster directly will fail due to dependency constraints.
   - First, select and delete the DB instance (`database-1-instance-1`), choosing to skip the final snapshot.
   - Second, select and delete the parent DB cluster (`database-1`).

> **Key Lesson:** Managed database clusters have strict dependency chains. You must always remove the reader and writer instances before the cluster metadata can be deleted.

---

### Day 1 Summary & Key Takeaways

- **Credits Secured:** Successfully claimed $100 in startup credits and earned an additional $100 by completing the 5 guided tasks (Total: **$200**).
- **Service Familiarity:** Gained hands-on experience deploying instances (EC2), configuring AI prompts (Bedrock), monitoring budgets (AWS Budgets), executing serverless functions (Lambda), and managing databases (RDS).
- **Cost Discipline:** Developed a strong habit of terminating resources immediately after deployment. A single database instance or VM left active can deplete credits rapidly.
- **Guided Exploration:** Using the AWS Console's guided tasks is a low-risk, structured method for testing new cloud services.

---

*Source: [First Cloud Journey - AWS Study Group](https://cloudjourney.awsstudygroup.com/)*
