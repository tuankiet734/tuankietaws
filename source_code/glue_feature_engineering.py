
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, FloatType, StringType
from pyspark.sql.window import Window

args = getResolvedOptions(sys.argv, [
    'JOB_NAME', 'db_host', 'db_name', 'db_user', 'db_pass'
])

sc          = SparkContext()
glueContext = GlueContext(sc)
spark       = glueContext.spark_session
job         = Job(glueContext)
job.init(args['JOB_NAME'], args)

DB_HOST = args['db_host']
DB_NAME = args['db_name']
DB_USER = args['db_user']
DB_PASS = args['db_pass']

JDBC_URL = f"jdbc:postgresql://{DB_HOST}:5432/{DB_NAME}"

# Props cho DOC du lieu (khong can batchsize)
JDBC_PROPS = {
    "user":       DB_USER,
    "password":   DB_PASS,
    "driver":     "org.postgresql.Driver",
    "ssl":        "true",
    "sslfactory": "org.postgresql.ssl.NonValidatingFactory"
}

# Props cho GHI du lieu: giam partition, them batchsize
JDBC_WRITE_PROPS = {
    "user":       DB_USER,
    "password":   DB_PASS,
    "driver":     "org.postgresql.Driver",
    "ssl":        "true",
    "sslfactory": "org.postgresql.ssl.NonValidatingFactory",
    "batchsize":  "10000",
    "numPartitions": "4"
}

# ══════════════════════════════════════════════════════
# HAM TIEN ICH
# ══════════════════════════════════════════════════════
def check_sku(df, step_name):
    """Kiem tra suc khoe SKU tai moi buoc - tra ve so null"""
    total    = df.count()
    null_sku = df.filter(
        F.col('sku').isNull() | (F.trim(F.col('sku').cast(StringType())) == '')
    ).count()
    ok  = total - null_sku
    pct = ok / total * 100 if total > 0 else 0
    print(f"[SKU] {step_name}: Total={total:,} | OK={ok:,} ({pct:.1f}%) | Null={null_sku:,}")
    return null_sku

def check_features(df, step_name, from_date='2023-01-08'):
    """Kiem tra cac features co gia tri hop le khong"""
    row = df.filter(F.col('date') >= from_date).agg(
        F.max('lag_1d').alias('max_lag1'),
        F.max('lag_7d').alias('max_lag7'),
        F.max('rolling_mean_7d').alias('max_roll'),
        F.max('s_sales_velocity').alias('max_vel'),
        F.avg('lag_1d').alias('avg_lag1'),
        F.avg('rolling_mean_7d').alias('avg_roll'),
        F.avg('s_sales_velocity').alias('avg_vel'),
        F.avg('total_lifespan').alias('avg_life'),
    ).collect()[0]

    print(f"\n[FEATURES] {step_name}:")
    print(f"  lag_1d:         max={row['max_lag1']:.1f}  avg={row['avg_lag1']:.3f}")
    print(f"  lag_7d:         max={row['max_lag7']:.1f}  avg={0:.3f}")
    print(f"  rolling_mean:   max={row['max_roll']:.1f}  avg={row['avg_roll']:.3f}")
    print(f"  s_sales_vel:    max={row['max_vel']:.1f}   avg={row['avg_vel']:.3f}")
    print(f"  total_lifespan: avg={row['avg_life']:.1f}")

    errors = []
    if row['max_lag1'] == 0:   errors.append("lag_1d=0 toan bo!")
    if row['max_lag7'] == 0:   errors.append("lag_7d=0 toan bo!")
    if row['max_roll'] == 0:   errors.append("rolling_mean=0 toan bo!")
    if row['max_vel']  == 0:   errors.append("s_sales_velocity=0 toan bo!")
    if row['avg_life'] == 0:   errors.append("total_lifespan=0 toan bo!")

    if errors:
        print(f"[FEATURES] CANH BAO: {', '.join(errors)}")
    else:
        print(f"[FEATURES] TAT CA FEATURES HOP LE - OK!")
    return len(errors) == 0

def fill_null_str(df, cols, default='UNKNOWN'):
    """Fill null cho nhieu cot string cung luc"""
    for c in cols:
        df = df.withColumn(c,
            F.when(F.col(c).isNull() | (F.trim(F.col(c)) == ''), F.lit(default))
             .otherwise(F.trim(F.col(c)))
        )
    return df

def fill_null_num(df, cols, default=0.0):
    """Fill null cho nhieu cot so cung luc"""
    return df.fillna({c: default for c in cols})


print("=" * 60)
print("[ETL] V5 - BAO VE SKU + TU KIEM TRA FEATURES")
print("=" * 60)


# ══════════════════════════════════════════════════════
# BUOC 1: DOC DATA TU RDS
# ══════════════════════════════════════════════════════
print("\n[ETL] BUOC 1: Doc data...")

df_tx     = spark.read.jdbc(JDBC_URL, "transactions", properties=JDBC_PROPS)
df_prod   = spark.read.jdbc(JDBC_URL, "products",     properties=JDBC_PROPS)
df_stores = spark.read.jdbc(JDBC_URL, "stores",       properties=JDBC_PROPS)

# Chuan hoa ten cot ve chu thuong
df_tx     = df_tx.toDF(*[c.lower()     for c in df_tx.columns])
df_prod   = df_prod.toDF(*[c.lower()   for c in df_prod.columns])
df_stores = df_stores.toDF(*[c.lower() for c in df_stores.columns])

print(f"[ETL] TX cols:    {df_tx.columns}")
print(f"[ETL] Prod cols:  {df_prod.columns}")
print(f"[ETL] Store cols: {df_stores.columns}")

# Them ngay
df_tx = df_tx.withColumn('tx_date', F.to_date(F.col('transaction_date')))


# ══════════════════════════════════════════════════════
# L1: BAO VE SKU - Luu sku_original NGAY KHI DOC
# ══════════════════════════════════════════════════════
print("\n[ETL] L1: Bao ve SKU goc...")
if 'sku' in df_tx.columns:
    df_tx = df_tx.withColumn('sku_original',
        F.when(
            F.col('sku').isNotNull() & (F.trim(F.col('sku').cast(StringType())) != ''),
            F.trim(F.col('sku').cast(StringType()))
        ).otherwise(F.lit(None).cast(StringType()))
    )
    n = df_tx.filter(F.col('sku_original').isNull()).count()
    print(f"[ETL] L1: sku_original null: {n:,} / {df_tx.count():,}")
else:
    df_tx = df_tx.withColumn('sku_original', F.lit(None).cast(StringType()))
    print("[ETL] L1: Khong co cot sku - se dung fallback")

# Loai returns + discount sai
df_tx = df_tx.filter(F.col('quantity') > 0)
df_tx = df_tx.withColumn('discount_pct',
    F.when(F.col('discount_pct') > 1.0, F.lit(0.0))
     .when(F.col('discount_pct') < 0.0, F.lit(0.0))
     .otherwise(F.col('discount_pct').cast(FloatType()))
)
df_tx = df_tx.withColumn('quantity', F.col('quantity').cast(IntegerType()))
df_tx = df_tx.filter(F.col('quantity').isNotNull() & (F.col('quantity') > 0))
df_tx.cache()

tx_count = df_tx.count()
print(f"[ETL] Transactions (sach): {tx_count:,}")
print(f"[ETL] Products:            {df_prod.count():,}")
print(f"[ETL] Stores:              {df_stores.count():,}")

# Lay range ngay
date_row = df_tx.agg(
    F.min('tx_date').alias('min_d'),
    F.max('tx_date').alias('max_d')
).collect()[0]
print(f"[ETL] Range: {date_row['min_d']} -> {date_row['max_d']}")


# ══════════════════════════════════════════════════════
# BUOC 2: XU LY SACH PRODUCTS
# ══════════════════════════════════════════════════════
print("\n[ETL] BUOC 2: Xu ly products...")

df_prod = df_prod.withColumn('price', F.col('price').cast(FloatType()))

# Fill null price bang median theo category
median_map = df_prod.groupBy('category').agg(
    F.percentile_approx('price', 0.5).alias('median_price')
)
df_prod = df_prod.join(median_map, on='category', how='left')
df_prod = df_prod.withColumn('price',
    F.when(F.col('price').isNull() | F.isnan('price'), F.col('median_price'))
     .otherwise(F.col('price'))
).fillna({'price': 50.0}).drop('median_price')
df_prod = df_prod.fillna({'currency': 'USD'})

# Fill null color bang mode theo category
mode_color = df_prod.groupBy('category', 'color').count() \
    .orderBy(F.col('count').desc()) \
    .groupBy('category').agg(F.first('color').alias('mode_color'))
df_prod = df_prod.join(mode_color, on='category', how='left')
df_prod = df_prod.withColumn('color',
    F.when(F.col('color').isNull(), F.col('mode_color'))
     .otherwise(F.col('color'))
).fillna({'color': 'UNKNOWN'}).drop('mode_color')

# Fill null size bang mode theo sub_category
mode_size = df_prod.groupBy('sub_category', 'size').count() \
    .orderBy(F.col('count').desc()) \
    .groupBy('sub_category').agg(F.first('size').alias('mode_size'))
df_prod = df_prod.join(mode_size, on='sub_category', how='left')
df_prod = df_prod.withColumn('size',
    F.when(F.col('size').isNull(), F.col('mode_size'))
     .otherwise(F.col('size'))
).fillna({'size': 'M'}).drop('mode_size')

# Tao color_type
df_prod = df_prod.withColumn('color_type',
    F.when(
        F.col('color').rlike('(?i)multi|/|estampado|listrado|xadrez|floral|print'),
        F.lit('Multi Color')
    ).otherwise(F.lit('Cor Unica'))
)

# Tinh usd_price
rate_map = F.create_map(
    F.lit('USD'), F.lit(1.00), F.lit('EUR'), F.lit(1.08),
    F.lit('GBP'), F.lit(1.27), F.lit('CNY'), F.lit(0.14),
    F.lit('BRL'), F.lit(0.20)
)
df_prod = df_prod.withColumn('usd_price',
    F.round(
        F.col('price') * F.coalesce(rate_map[F.col('currency')], F.lit(1.0)),
        2
    )
)

# Doi ten sku_prod tranh xung dot
df_prod = df_prod.withColumnRenamed('sku', 'sku_prod') \
    if 'sku' in df_prod.columns \
    else df_prod.withColumn('sku_prod', F.lit(None).cast(StringType()))

df_prod = df_prod.withColumn('product_id_str', F.col('product_id').cast(StringType()))
df_prod.cache()
print("[ETL] Products xong. Null usd_price:", df_prod.filter(F.col('usd_price').isNull()).count())


# ══════════════════════════════════════════════════════
# BUOC 3: XU LY STORES
# ══════════════════════════════════════════════════════
print("\n[ETL] BUOC 3: Xu ly stores...")

df_stores = fill_null_str(df_stores, ['country', 'city'], 'Unknown')
store_stats = df_tx.groupBy('store_id').agg(
    F.countDistinct('product_id').alias('num_distinct_products'),
    F.countDistinct('sku_original').alias('num_distinct_skus')
)
df_stores = df_stores.join(store_stats, on='store_id', how='left')
df_stores = fill_null_num(df_stores, ['num_distinct_products', 'num_distinct_skus'], 0)
df_stores.cache()
print("[ETL] Stores xong.")


# ══════════════════════════════════════════════════════
# BUOC 4: JOIN 3 BANG + L2-L5 BAO VE SKU
# ══════════════════════════════════════════════════════
print("\n[ETL] BUOC 4: Join + bao ve SKU L2-L5...")

df_prod_sel = df_prod.select(
    'product_id', 'sku_prod', 'product_id_str',
    'color', 'size', 'color_type', 'category', 'sub_category', 'usd_price'
)
df_stores_sel = df_stores.select(
    'store_id', 'country', 'city', 'num_distinct_products', 'num_distinct_skus'
)

df_joined = df_tx \
    .join(df_prod_sel,   on='product_id', how='left') \
    .join(df_stores_sel, on='store_id',   how='left')

# L2 -> L5: chon SKU theo thu tu uu tien
df_joined = df_joined.withColumn('sku',
    F.when(
        # L2: sku tu products
        F.col('sku_prod').isNotNull() & (F.trim(F.col('sku_prod')) != ''),
        F.trim(F.col('sku_prod'))
    ).when(
        # L3: sku goc tu transactions
        F.col('sku_original').isNotNull() & (F.trim(F.col('sku_original')) != ''),
        F.trim(F.col('sku_original'))
    ).when(
        # L4: build tu product_id + size + color
        F.col('product_id').isNotNull(),
        F.concat_ws('-',
            F.lit('SKU'),
            F.col('product_id').cast(StringType()),
            F.coalesce(F.trim(F.col('size')),  F.lit('UNK')),
            F.coalesce(F.trim(F.col('color')), F.lit('UNK'))
        )
    ).otherwise(F.col('product_id_str'))  # L5: last resort
)
# Dam bao tuyet doi khong null
df_joined = df_joined.withColumn('sku',
    F.coalesce(F.col('sku'), F.lit('SKU-UNKNOWN'))
)

# Fill null cac cot khac
df_joined = fill_null_str(df_joined,
    ['color','size','color_type','category','sub_category','country','city'],
    'Unknown'
)
df_joined = fill_null_num(df_joined, ['discount_pct', 'usd_price'], 0.0)

# Drop cot tam
df_joined = df_joined.drop('sku_original', 'sku_prod', 'product_id_str')
df_joined.cache()

# Kiem tra SKU
null_after = check_sku(df_joined, "Sau join")
if null_after == 0:
    print("[ETL] HOAN HAO: Khong co SKU null!")
else:
    print(f"[ETL] Van con {null_after} null - da duoc phu luoi cuoi")
    df_joined = df_joined.fillna({'sku': 'SKU-UNKNOWN'})


# ══════════════════════════════════════════════════════
# BUOC 5: DAILY AGGREGATION
# ══════════════════════════════════════════════════════
print("\n[ETL] BUOC 5: Daily aggregation...")

daily = df_joined.groupBy('store_id', 'sku', 'tx_date').agg(
    F.sum('quantity').cast(FloatType()).alias('qty'),
    F.round(F.avg('usd_price'),   2).alias('avg_usd_price'),
    F.round(F.avg('discount_pct'),4).alias('total_discount_avg'),
    F.first('product_id').alias('product_id'),
    F.first('color').alias('color'),
    F.first('size').alias('size'),
    F.first('color_type').alias('color_type'),
    F.first('category').alias('category'),
    F.first('sub_category').alias('sub_category'),
    F.first('country').alias('country'),
    F.first('city').alias('city'),
    F.first('num_distinct_products').alias('num_distinct_products'),
    F.first('num_distinct_skus').alias('num_distinct_skus'),
)
daily = fill_null_num(daily, ['total_discount_avg', 'avg_usd_price', 'qty'], 0.0)
daily = fill_null_str(daily, ['color','size','color_type','category','sub_category','country','city'], 'Unknown')

# Doi ten + them date_int de Window tinh toan
daily = daily.withColumnRenamed('tx_date', 'date')
daily = daily.withColumn('date_int',
    F.datediff(F.col('date'), F.lit('1970-01-01'))
)

# Dam bao qty > 0 (loai ngay bi aggregate sai)
daily = daily.filter(F.col('qty') > 0)

daily.cache()
total_daily = daily.count()
print(f"[ETL] daily records: {total_daily:,}")
check_sku(daily, "Daily")

# Kiem tra phan bo qty de dam bao data hop le
qty_stats = daily.agg(
    F.min('qty').alias('min_qty'),
    F.max('qty').alias('max_qty'),
    F.avg('qty').alias('avg_qty'),
    F.countDistinct('date').alias('so_ngay'),
    F.countDistinct('store_id').alias('so_store'),
    F.countDistinct('sku').alias('so_sku'),
).collect()[0]
print(f"[ETL] qty: min={qty_stats['min_qty']:.0f} max={qty_stats['max_qty']:.0f} avg={qty_stats['avg_qty']:.1f}")
print(f"[ETL] Ngay: {qty_stats['so_ngay']} | Stores: {qty_stats['so_store']} | SKUs: {qty_stats['so_sku']}")


# ══════════════════════════════════════════════════════
# BUOC 6: COVERAGE & LIFESPAN
# ══════════════════════════════════════════════════════
print("\n[ETL] BUOC 6: Coverage va lifespan...")

sku_cov = daily.groupBy('sku').agg(
    F.countDistinct('store_id').alias('sku_store_coverage')
)
prod_cov = daily.groupBy('product_id').agg(
    F.countDistinct('store_id').alias('product_store_coverage')
)
first_global = daily.groupBy('sku').agg(F.min('date').alias('first_global_date'))
first_store  = daily.groupBy('store_id', 'sku').agg(F.min('date').alias('first_store_date'))

daily = daily \
    .join(sku_cov,      on='sku',               how='left') \
    .join(prod_cov,     on='product_id',        how='left') \
    .join(first_global, on='sku',               how='left') \
    .join(first_store,  on=['store_id', 'sku'], how='left')

daily = daily \
    .withColumn('total_lifespan',
        F.datediff(F.col('date'), F.col('first_global_date')).cast(FloatType())
    ) \
    .withColumn('s_total_lifespan',
        F.datediff(F.col('date'), F.col('first_store_date')).cast(FloatType())
    )
daily = fill_null_num(daily,
    ['sku_store_coverage','product_store_coverage','total_lifespan','s_total_lifespan'],
    0.0
)
daily = daily.withColumn('sku_store_coverage',
    F.when(F.col('sku_store_coverage') < 1, F.lit(1.0))
     .otherwise(F.col('sku_store_coverage').cast(FloatType()))
)
daily = daily.withColumn('product_store_coverage',
    F.when(F.col('product_store_coverage') < 1, F.lit(1.0))
     .otherwise(F.col('product_store_coverage').cast(FloatType()))
)
print("[ETL] Coverage va lifespan xong.")


# ══════════════════════════════════════════════════════
# BUOC 7: LAG FEATURES - WINDOW FUNCTIONS
# QUAN TRONG: Window partitionBy store_id + sku
#             orderBy date_int (so nguyen, khong phai date string)
# ══════════════════════════════════════════════════════
print("\n[ETL] BUOC 7: Lag features (Window)...")

w_sku = Window.partitionBy('store_id', 'sku').orderBy('date_int')

daily = daily \
    .withColumn('lag_1d', F.lag('qty', 1, 0.0).over(w_sku).cast(FloatType())) \
    .withColumn('lag_7d', F.lag('qty', 7, 0.0).over(w_sku).cast(FloatType()))
daily = fill_null_num(daily, ['lag_1d', 'lag_7d'], 0.0)

# Kiem tra ngay sau khi tinh lag
sample = daily.filter(
    (F.col('store_id') == 1) & (F.col('date') >= '2023-01-08')
).select('date','sku','qty','lag_1d','lag_7d') \
 .orderBy('date','sku').limit(3).collect()
print("[ETL] Lag sample (store_id=1):")
for r in sample:
    flag = "OK" if r['lag_1d'] > 0 else "ZERO!"
    print(f"  {r['date']} | sku={str(r['sku'])[:25]:25s} | qty={r['qty']:6.0f} | lag1={r['lag_1d']:6.0f} | lag7={r['lag_7d']:6.0f} [{flag}]")

print("[ETL] Lag xong.")


# ══════════════════════════════════════════════════════
# BUOC 8: ROLLING 7 NGAY - WINDOW FUNCTIONS
# rangeBetween(-7, -1): 7 ngay truoc, KHONG tinh ngay hom nay
# ══════════════════════════════════════════════════════
print("\n[ETL] BUOC 8: Rolling 7 ngay...")

w_roll7 = Window.partitionBy('store_id', 'sku') \
    .orderBy('date_int').rangeBetween(-7, -1)

daily = daily \
    .withColumn('rolling_mean_7d',
        F.round(F.avg('qty').over(w_roll7), 4).cast(FloatType())
    ) \
    .withColumn('rolling_std_7d',
        F.round(F.stddev('qty').over(w_roll7), 4).cast(FloatType())
    )
daily = fill_null_num(daily, ['rolling_mean_7d', 'rolling_std_7d'], 0.0)
print("[ETL] Rolling xong.")


# ══════════════════════════════════════════════════════
# BUOC 9: VELOCITY - WINDOW FUNCTIONS
# ══════════════════════════════════════════════════════
print("\n[ETL] BUOC 9: Velocity features...")

w30 = Window.partitionBy('store_id','sku').orderBy('date_int').rangeBetween(-30,-1)
w7  = Window.partitionBy('store_id','sku').orderBy('date_int').rangeBetween(-7, -1)

# 30 ngay
daily = daily \
    .withColumn('s_days_active',        F.count('qty').over(w30).cast(FloatType())) \
    .withColumn('s_selling_days_count', F.count('qty').over(w30).cast(FloatType())) \
    .withColumn('_q30', F.sum('qty').over(w30)) \
    .withColumn('s_sales_velocity',
        F.round(F.col('_q30') / F.greatest(F.col('s_days_active'), F.lit(1.0)), 4)
         .cast(FloatType())
    ).drop('_q30')

# 7 ngay
daily = daily \
    .withColumn('s2_days_active',        F.count('qty').over(w7).cast(FloatType())) \
    .withColumn('s2_selling_days_count', F.count('qty').over(w7).cast(FloatType())) \
    .withColumn('_q7', F.sum('qty').over(w7)) \
    .withColumn('s2_sales_velocity',
        F.round(F.col('_q7') / F.greatest(F.col('s2_days_active'), F.lit(1.0)), 4)
         .cast(FloatType())
    ).drop('_q7')

daily = fill_null_num(daily, [
    's_days_active','s_selling_days_count','s_sales_velocity',
    's2_days_active','s2_selling_days_count','s2_sales_velocity'
], 0.0)
print("[ETL] Velocity xong.")


# ══════════════════════════════════════════════════════
# BUOC 10: CHUAN BI OUTPUT
# ══════════════════════════════════════════════════════
print("\n[ETL] BUOC 10: Chuan bi output...")

daily = daily \
    .withColumn('store_id',   F.col('store_id').cast(IntegerType())) \
    .withColumn('product_id', F.col('product_id').cast(IntegerType()))

final_cols = [
    'store_id','sku','date','product_id',
    'size','color','color_type','category','sub_category',
    'country','city',
    'num_distinct_products','num_distinct_skus',
    'avg_usd_price','total_discount_avg',
    'total_lifespan','s_total_lifespan',
    'sku_store_coverage','product_store_coverage',
    's_days_active','s_selling_days_count','s_sales_velocity',
    's2_days_active','s2_selling_days_count','s2_sales_velocity',
    'lag_1d','lag_7d',
    'rolling_mean_7d','rolling_std_7d'
]

missing = [c for c in final_cols if c not in daily.columns]
if missing:
    print(f"[ETL] LOI NGHIEM TRONG: Thieu cot {missing} - DUNG LAI!")
    job.commit()
    sys.exit(1)

final_df = daily.select(final_cols)
total_records = final_df.count()
print(f"[ETL] Tong records: {total_records:,}")

# Kiem tra toan dien cuoi cung
null_sku_final = check_sku(final_df, "KIEM TRA CUOI")
features_ok    = check_features(final_df, "KIEM TRA CUOI")

# Bao cao tong ket chat luong
print(f"\n[ETL] ══ BAO CAO CHAT LUONG ══")
print(f"  Records:         {total_records:,}")
print(f"  SKU null:        {null_sku_final:,}  ({'OK' if null_sku_final == 0 else 'CO VAN DE'})")
print(f"  Features:        {'TAT CA OK' if features_ok else 'CO VAN DE - xem log tren'}")


# ══════════════════════════════════════════════════════
# BUOC 11: GHI VAO RDS (DA SUA: coalesce + batchsize)
# ══════════════════════════════════════════════════════
print(f"\n[ETL] BUOC 11: Ghi {total_records:,} records vao final_daily...")

# Giam partition xuong 4, dung JDBC_WRITE_PROPS co batchsize
final_df.coalesce(4).write.jdbc(
    JDBC_URL, 'final_daily',
    mode='append',
    properties=JDBC_WRITE_PROPS
)

print("=" * 60)
print(f"[ETL] HOAN THANH! {total_records:,} records da ghi vao final_daily.")
print(f"[ETL] SKU null: {null_sku_final:,} | Features: {'OK' if features_ok else 'COI LAI LOG'}")
print("=" * 60)


# ══════════════════════════════════════════════════════
# BUOC 12: GHI VAO TRAINING RDS (training_db)
# ══════════════════════════════════════════════════════
print(f"\n[ETL] BUOC 12: Ghi {total_records:,} records vao training_db (final_daily)...")

TRAINING_DB_HOST = "training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
TRAINING_DB_NAME = "fashiondb"
TRAINING_JDBC_URL = f"jdbc:postgresql://{TRAINING_DB_HOST}:5432/{TRAINING_DB_NAME}"

# Giam partition xuong 4, dung JDBC_WRITE_PROPS co batchsize
final_df.coalesce(4).write.jdbc(
    TRAINING_JDBC_URL, 'final_daily',
    mode='append',
    properties=JDBC_WRITE_PROPS
)

print("=" * 60)
print(f"[ETL] HOAN THANH BUOC 12: {total_records:,} records da ghi vao training_db.final_daily.")
print("=" * 60)

job.commit()