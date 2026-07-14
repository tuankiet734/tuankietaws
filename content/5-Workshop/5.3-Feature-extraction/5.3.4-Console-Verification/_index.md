---
title: "Console Verification"
date: 2024-07-07
weight: 4
chapter: false
pre: " <b> 5.3.4. </b> "
---

### 5.3.4. Console Verification Proofs

Validate Glue job executions and check details:

#### Verification Steps:
1. Navigate to **AWS Glue Studio** -> **ETL jobs**.
2. Review the execution history list for both `de-fashion-rds-extract` and `glue_feature_engineering.py`.
3. Confirm that the **Run status** column displays **Succeeded**.
4. Open the **Amazon CloudWatch Logs** link to check the output prints:
   * For the extraction job: `Extract thanh cong!`
   * For the feature engineering job: Quality report prints `[FEATURES] TAT CA FEATURES HOP LE - OK!` alongside the total records processed.

##### Screenshot Guide:
* Capture a screenshot of the Glue Jobs console page showing these jobs and save the image at: `static/AWS/images/5-Workshop/5.3-Feature-extraction/glue-jobs.png` and remove the comment markdown tags.

![Glue Jobs](/AWS/images/5-Workshop/5.3-Feature-extraction/glue-jobs.png)
