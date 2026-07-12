---
title: "Spark Feature Engineering Script"
date: 2024-07-07
weight: 3
chapter: false
pre: " <b> 5.3.3. </b> "
---

### 5.3.3. Spark Feature Engineering Script (`glue_feature_engineering.py`)

The heavy-duty computations are calculated using **Apache Spark** running on **AWS Glue** to process large datasets.

##### Core PySpark Snippets:

#### 1. Lag Sales Features:
Window functions partition by outlet and item (`store_id`, `sku`) and sort by time index to calculate lagged history:
```python
w_sku = Window.partitionBy('store_id', 'sku').orderBy('date_int')

daily = daily \
    .withColumn('lag_1d', F.lag('qty', 1, 0.0).over(w_sku).cast(FloatType())) \
    .withColumn('lag_7d', F.lag('qty', 7, 0.0).over(w_sku).cast(FloatType()))
```

#### 2. Rolling averages:
Computes average sales and sales deviation over a moving 7-day lookback window:
```python
w_roll7 = Window.partitionBy('store_id', 'sku') \
    .orderBy('date_int').rangeBetween(-7, -1)

daily = daily \
    .withColumn('rolling_mean_7d',
        F.round(F.avg('qty').over(w_roll7), 4).cast(FloatType())
    ) \
    .withColumn('rolling_std_7d',
        F.round(F.stddev('qty').over(w_roll7), 4).cast(FloatType())
    )
```

#### 3. Sales Velocity:
Measures active days and sales velocities in 30-day and 7-day windows:
```python
w30 = Window.partitionBy('store_id','sku').orderBy('date_int').rangeBetween(-30,-1)

daily = daily \
    .withColumn('s_days_active',        F.count('qty').over(w30).cast(FloatType())) \
    .withColumn('s_selling_days_count', F.count('qty').over(w30).cast(FloatType())) \
    .withColumn('_q30', F.sum('qty').over(w30)) \
    .withColumn('s_sales_velocity',
        F.round(F.col('_q30') / F.greatest(F.col('s_days_active'), F.lit(1.0)), 4)
         .cast(FloatType())
    ).drop('_q30')
```

#### 4. Write to Targets:
```python
# Write to Central DB
final_df.coalesce(4).write.jdbc(
    JDBC_URL, 'final_daily',
    mode='append',
    properties=JDBC_WRITE_PROPS
)

# Write to Training DB
final_df.coalesce(4).write.jdbc(
    TRAINING_JDBC_URL, 'final_daily',
    mode='append',
    properties=JDBC_WRITE_PROPS
)
```
