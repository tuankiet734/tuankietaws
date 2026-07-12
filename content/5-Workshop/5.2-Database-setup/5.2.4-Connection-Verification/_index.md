---
title: "Connection Verification"
date: 2024-07-07
weight: 4
chapter: false
pre: " <b> 5.2.4. </b> "
---

### 5.2.4. Connection Verification

Once database initialization and security settings are complete, verify connectivity to ensure subsequent pipelines can interact with the databases without connection blockages.

#### Method 1: Using Command-Line Tool (`psql`)
Connect to the PostgreSQL shell interface using the standard CLI tools:

##### Connect to Central DB:
```bash
psql -h fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com -p 5432 -U dbadmin -d fashiondb
```

##### Connect to Training DB:
```bash
psql -h training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com -p 5432 -U dbadmin -d fashiondb
```

If you are prompted for a password and log in successfully to the `fashiondb=>` prompt, your databases are ready.

---

#### Method 2: Using pgAdmin or DBeaver
1. Open your database administration client.
2. Setup a new **PostgreSQL** connection.
3. Supply the connection parameters:
   * **Host:** Insert the corresponding database endpoint.
   * **Port:** `5432`
   * **Database:** `fashiondb`
   * **Username:** `dbadmin`
   * **Password:** Database account password.
4. Click **Test Connection**. When connection status displays success, save connection profiles.
