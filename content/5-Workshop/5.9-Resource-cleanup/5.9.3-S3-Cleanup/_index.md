---
title: "S3 Bucket Removal"
date: 2024-07-07
weight: 3
chapter: false
pre : " <b> 5.9.3. </b> "
---

### 5.9.3. Purging and Deleting Amazon S3 Buckets

Amazon S3 requires all objects inside a bucket to be permanently deleted before the bucket itself can be removed. Follow the steps below:

1. Open the **Amazon S3 Console**.
2. Locate and click on the machine learning model storage bucket: `fashion-retail-model-storage` (or the GenAI product images bucket, e.g., `fashion-product-images-group3979`).
3. Click the **Empty** button at the top menu:
   * Type `permanently delete` in the confirmation box to confirm purging all objects (including `.pkl` files in the `models/` directory).
   * Click **Empty** to complete the purge.
4. Go back to the Buckets list, select the emptied bucket, and click the **Delete** button:
   * Type the exact bucket name to confirm deletion.
   * Click **Delete bucket** to release the resource.

---

#### Verification on Amazon S3:

![Delete S3](/images/5-Workshop/5.9-Resource-cleanup/delete-s3.png)

