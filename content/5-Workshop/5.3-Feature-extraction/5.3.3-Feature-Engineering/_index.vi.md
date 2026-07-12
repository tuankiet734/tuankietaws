---
title: "Script Spark ETL kỹ nghệ đặc trưng"
date: 2024-07-07
weight: 3
chapter: false
pre: " <b> 5.3.3. </b> "
---

### 5.3.3. Script Spark ETL Kỹ nghệ Đặc trưng (`glue_feature_engineering.py`)

Tác vụ chính được thực hiện bằng **Apache Spark** trên **AWS Glue** để tính toán các đặc trưng chuỗi thời gian cho hàng triệu điểm dữ liệu.

##### Phân đoạn mã nguồn Spark SQL cốt lõi:

#### 1. Trích xuất đặc trưng trễ (Lags):
Tính toán lượng hàng đã bán trong quá khứ ($t-1$ và $t-7$) để mô hình nắm bắt được xu hướng tiêu thụ gần nhất:
```python
w_sku = Window.partitionBy('store_id', 'sku').orderBy('date_int')

daily = daily \
    .withColumn('lag_1d', F.lag('qty', 1, 0.0).over(w_sku).cast(FloatType())) \
    .withColumn('lag_7d', F.lag('qty', 7, 0.0).over(w_sku).cast(FloatType()))
```

#### 2. Tính trung bình trượt (Rolling statistics):
Tính trung bình doanh số và độ lệch chuẩn doanh số của sản phẩm trong vòng 7 ngày gần nhất:
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

#### 3. Tính tốc độ bán hàng (Sales Velocity):
Đo lường số ngày sản phẩm bán được hàng trong vòng 30 ngày và tính tỷ lệ bán hàng trung bình mỗi ngày:
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

#### 4. Tải dữ liệu đặc trưng xuống cả hai Databases qua JDBC:
```python
# Ghi vào Central DB
final_df.coalesce(4).write.jdbc(
    JDBC_URL, 'final_daily',
    mode='append',
    properties=JDBC_WRITE_PROPS
)

# Ghi vào Training DB
final_df.coalesce(4).write.jdbc(
    TRAINING_JDBC_URL, 'final_daily',
    mode='append',
    properties=JDBC_WRITE_PROPS
)
```
