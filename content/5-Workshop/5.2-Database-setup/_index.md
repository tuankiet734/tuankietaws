---
title : "Database Setup"
date : 2024-07-07
weight : 2
chapter : false
pre : " <b> 5.2. </b> "
---

To prepare data storage for the entire system, we deploy two parallel **Amazon RDS PostgreSQL** relational databases on AWS: a central database for live transactions (`fashion-rds`) and a dedicated database for processed ML feature tables (`training-db`).

---

{{% children /%}}
