---
title: "EC2 Resource Cleanup"
date: 2024-07-07
weight: 1
chapter: false
pre : " <b> 5.9.1. </b> "
---

### 5.9.1. EC2 Resource Cleanup

To avoid ongoing computational costs from virtual machines and their attached EBS storage volumes, perform the cleanup steps below:

1. Open the **Amazon EC2 Console** -> **Instances**.
2. Locate and check the checkboxes for the following project instances:
   * `Web-Application-Server` (Kiet's Frontend Server)
   * `fashion-api-server` (Tung's RESTful API Server)
   * `ML-Forecast-Server` (Thanh's Machine Learning Server)
3. Click the **Instance state** button at the top menu -> Select **Terminate instance**.
4. Confirm by clicking **Terminate** in the confirmation pop-up.

> [!NOTE]
> * The instance states will transition to `Shutting-down` and eventually to `Terminated`.
> * Attached EBS (Elastic Block Store) volumes configured with "Delete on termination" will be automatically deleted to prevent persistent storage fees.
