---
title: "Day 2"
date: 2026-06-08
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
---

# Work Log: Advanced Cost Auditing, Multi-Tier Monitoring, and Core Infrastructure Concepts

> **Day 2 - Monday, June 08, 2026:** Designed a multi-layered cost alerting system, established an operational emergency response protocol, and studied core cloud architecture and security principles.

---

### Objectives for the Day

- Implement a **Multi-Level Monitoring System** to prevent unexpected billing.
- Deploy **Cost Anomaly Detection** and resource tagging policies for granular expense tracking.
- Document an **Emergency Cost Control Runbook** featuring AWS CLI audit commands.
- Study core AWS theoretical concepts: Global Infrastructure, Identity and Access Management (IAM), and Shared Responsibility.

---

### Multi-Level Monitoring & Billing Safeguards

#### 1. Three-Tier AWS Budget Thresholds

To ensure comprehensive cost visibility, I established three distinct budgets in the billing dashboard:

| Alert Identity | Target Limit | Condition for Alert |
|---|---|---|
| **Monthly Cap Budget** | $40.00 / month | Alert at 80% ($32.00) actual spend |
| **Warning Budget** | $20.00 / month | Alert at 50% ($10.00) actual spend |
| **Daily Safeguard Budget** | $5.00 / day | Alert at 100% ($5.00) actual spend |

The daily budget acts as a rapid-response check, detecting runaway workloads within 24 hours rather than allowing costs to accumulate over a month.

#### 2. CloudWatch Billing Alarms

I configured Billing Alarms in the CloudWatch console using Amazon SNS to route notifications through escalating communication channels:

| Expense Target | Notification Method | Operational Action |
|---|---|---|
| **$15.00** | Email Notification | Standard alert; check active services. |
| **$35.00** | Email + SMS Alert | High priority; verify resource status. |
| **$60.00** | Email + SMS + Discord Hook | Emergency alert; initiate resource teardown protocol. |

#### 3. AWS Cost Anomaly Detection (New Feature Added)

Activated **AWS Cost Anomaly Detection** using a subscription monitor. This service applies machine learning algorithms to historical usage patterns to detect unusual spending spikes:
- Monitor Type: AWS Services.
- Alert Threshold: $5.00 daily impact.
- Outcome: Sends immediate notifications upon detecting abnormal spending trends, bypassing standard static budget limits.

---

### Advanced Cost Analytics & Custom Instrumentation

#### Resource Tagging Scheme

To organize cost allocation reports, I implemented a strict tagging policy for all provisioned infrastructure. This enables granular cost tracking by project, deployment stage, and author in AWS Cost Explorer:

| Tag Key | Example Value | Description |
|---|---|---|
| `Project` | `cloud-training` | Associates resources with a specific project. |
| `Environment` | `dev` / `testing` | Distinguishes development sandboxes from testing stages. |
| `Author` | `intern-dev` | Identifies the engineer responsible for resource creation. |

#### CloudWatch Metrics & Dashboards

- Created a consolidated **Cost & Health Dashboard** in CloudWatch, graphing EC2 CPU metrics alongside monthly estimated billing charges.
- Monitored application-level metrics to ensure test scripts did not enter infinite loops or generate redundant API calls.

---

### Emergency Cost Control & Cleanup Protocol

#### 1. CLI Resource Discovery Commands

When an anomaly detection or billing alert is triggered, run these diagnostic CLI commands to identify active, high-cost resources:

```bash
# 1. List all active EC2 instances across the current region
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].{ID:InstanceId,Type:InstanceType,Zone:Placement.AvailabilityZone}' \
  --output table

# 2. Identify all running database instances and their operational state
aws rds describe-db-instances \
  --query 'DBInstances[].{DBIdentifier:DBInstanceIdentifier,Engine:Engine,Status:DBInstanceStatus}' \
  --output table

# 3. Locate unattached EBS volumes (incurring costs while idle)
aws ec2 describe-volumes --filters "Name=status,Values=available" \
  --query 'Volumes[].{VolumeID:VolumeId,Size:Size,Zone:AvailabilityZone}' \
  --output table

# 4. Search for unassociated Elastic IP addresses (incurring hourly idle charges)
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].{IP:PublicIp,AllocationId:AllocationId}' \
  --output table
```

#### 2. Emergency Shutdown Runbook
1. Access the console via the Root or Administrator account.
2. Stop or terminate running virtual machines (`EC2`) and delete idle database clusters (`RDS`).
3. Delete unattached block store volumes (`EBS`) and release idle static IPs (`Elastic IPs`).
4. Disable active model playground configurations and delete unused serverless routes.

---

### Foundational Cloud Architecture Concepts

#### Cloud Computing Characteristics & Service Models
- **Elasticity:** The ability to scale resources dynamically matching demand variations.
- **OpEx vs. CapEx:** Shifting from capital expenses (buying physical datacenters) to operational expenses (paying for resources as they are consumed).
- **Global Deployment:** Launching systems near end-users to reduce latency.

| Service Model | AWS Example | User Responsibility |
|---|---|---|
| **IaaS (Infrastructure as a Service)** | Amazon EC2, VPC | Operating system configuration, runtime environments, application code. |
| **PaaS (Platform as a Service)** | AWS Elastic Beanstalk, RDS | Application code deployment and data schema definitions. |
| **SaaS (Software as a Service)** | Amazon WorkMail, Chime | No infrastructure management; access the application directly. |

#### AWS Global Infrastructure
- **Regions:** Geographically isolated hubs containing multiple data centers. Data residency is guaranteed within the selected region unless replicated by the user.
- **Availability Zones (AZs):** Distinct physical data centers within a Region, connected by low-latency fiber links. Deploying across multiple AZs ensures **High Availability**.
- **Edge Locations:** Points of presence that cache static content closer to users via the Amazon CloudFront CDN, reducing latency.

---

### Security, Identity, & Access Management (IAM)

- **The Shared Responsibility Model:**
  - **Security OF the Cloud:** AWS manages the physical security of data centers, virtualization layers, and global hardware.
  - **Security IN the Cloud:** The customer manages OS patches, network security groups, IAM credentials, and data encryption.
- **IAM Best Practices:**
  - **Protect the Root Account:** Require MFA and avoid using the root account for daily operational tasks.
  - **Principle of Least Privilege:** Grant users the minimum permissions required to perform their roles.
  - **Group-Based Policies:** Assign IAM policies to Groups rather than individual users for easier management.
  - **JSON Security Policies:** Define precise access rules by specifying allowed Actions, Resources, and Conditions.

---

### Core Storage & Database Services

- **Amazon S3 (Simple Storage Service):**
  - Object-based storage designed for **99.999999999% (11 nines) durability**.
  - Utilizes storage tiers (S3 Standard, Standard-IA, Glacier) to optimize storage costs based on data access frequency.
- **Amazon RDS:** Relational database service that automates backups, security patching, and replica synchronization.
- **AWS Lambda:** Event-driven compute service that executes code without server management, scaling dynamically.

---

### Study Schedule & Topics Completed

| Study Date | Core Topic Focus | Primary AWS Services Involved |
|---|---|---|
| **08/06/2026** | Compute Architecture & Scalability | Amazon EC2, AMI, Instance Types |
| **08/06/2026** | Access Delegation & Policy Structuring | AWS IAM, Roles, Policies |
| **08/06/2026** | Integrated Development Environments | AWS Cloud9, Instance Profiles |
| **08/06/2026** | Object Storage & Web Hosting | Amazon S3, S3 Bucket Policies |
| **08/06/2026** | Managed Databases & Backups | Amazon RDS, DB Engines |

---

### Day 2 Key Takeaways

1. **Defense-in-Depth Cost Strategy:** A layered alerting system (Budgets + Billing Alarms + Anomaly Detection) provides comprehensive coverage against unexpected charges.
2. **Tagging Integrity:** Resource tagging is essential for cost management; untagged resources make it difficult to trace billing anomalies.
3. **Operational Readiness:** Establishing an emergency cleanup runbook and using CLI commands to detect idle resources (like unattached EBS volumes and Elastic IPs) are key practices for maintaining a cost-efficient cloud environment.

---

*Source: [First Cloud Journey - AWS Study Group](https://cloudjourney.awsstudygroup.com/)*
