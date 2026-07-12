---
title: "EC2 Instance Termination"
date: 2024-07-07
weight: 1
chapter: false
pre: " <b> 5.6.1. </b> "
---

### 5.6.1. Terminating Amazon EC2 Compute Instances

1. Open the **Amazon EC2 Console** and click **Instances**.
2. Select the instances: `Web-Application-Server`, `fashion-api-server`, and `ML-Forecast-Server` (or delete their parent Auto Scaling Groups).
3. Click **Instance state** -> Select **Terminate instance** to delete the compute servers and release their associated EBS volumes.
