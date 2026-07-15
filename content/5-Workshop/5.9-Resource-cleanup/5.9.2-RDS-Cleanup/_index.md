---
title: "RDS Database Deletion"
date: 2024-07-07
weight: 2
chapter: false
pre : " <b> 5.9.2. </b> "
---

### 5.9.2. Deleting Amazon RDS Database Instances

To release the persistent database instances and stop incurring pricing charges, delete the RDS instances:

1. Open the **Amazon RDS Console** -> **Databases**.
2. Locate and check the boxes for:
   * `fashion-rds` (Main Business Database)
   * `training-db` (ML Feature Store/Training Database)
3. Click the **Actions** dropdown menu -> Select **Delete**.
4. In the deletion confirmation page:
   * **Uncheck** the box for *Create final snapshot?* (to avoid persistent storage fees for snapshots).
   * **Uncheck** the box for *Retain automated backups*.
   * Check the acknowledgment checkbox: *I acknowledge that upon deletion, automated backups, including system snapshots and point-in-time recovery, will no longer be available.*
   * Type `delete me` in the confirmation text box.
5. Click **Delete** to release the resources.

> [!WARNING]
> Deleting RDS databases will permanently erase all transaction history tables, precalculated feature records (`final_daily`), and predicted demand outputs. Make sure to export necessary datasets to local CSV files if needed for report references before proceeding.

