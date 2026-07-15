---
title: "Proof of Operation"
date: 2024-07-07
weight: 4
chapter: false
pre : " <b> 5.4.4. </b> "
---

### 5.4.4. Proof of Glue ETL Operation on AWS Console

We verify that the Glue jobs ran successfully and logged execution completion reports.

---

#### Step-by-Step Validation:

1. **Open AWS Glue Studio:** Select **ETL jobs** on the left menu.
2. **Select Job:** Click on either `de-fashion-rds-extract` or `glue_feature_engineering.py`.
3. **Verify Execution History (Runs):** Click the **Runs** tab.
4. **Check Status:** Verify that the **Run status** column displays **Succeeded** (with a green checkmark).
5. **View Logs:** Click **Output logs** to open CloudWatch Logs and inspect the print statements to confirm execution success.

---

#### AWS Console Proof of Operation:

Below is the screenshot showing the run logs and history of the AWS Glue Jobs:

![Glue Jobs](/images/5-Workshop/5.4-Feature-extraction/glue-run-succeeded.png)