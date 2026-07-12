---
title: "XGBoost Training Script"
date: 2024-07-07
weight: 2
chapter: false
pre: " <b> 5.4.2. </b> "
---

### 5.4.2. Machine Learning Training Script (Python ML Script)

A Python script runs on the EC2 machine, connecting to `training-db`, downloading feature records from the `final_daily` table, pre-processing arrays, and training an **XGBoost Regressor** model.

##### Core ML Code Snippet:
```python
import pandas as pd
import xgboost as xgb
from sqlalchemy import create_engine
import pickle
import boto3

# 1. Connect to the feature training database
db_url = "postgresql+psycopg2://dbadmin:Tung2004@training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com:5432/fashiondb"
engine = create_engine(db_url)
df = pd.read_sql("SELECT * FROM final_daily", engine)

# Sort and clean dataset
df = df.sort_values(by=['store_id', 'sku', 'date'])
features = [
    'avg_usd_price', 'total_discount_avg', 'total_lifespan', 's_total_lifespan',
    'sku_store_coverage', 'product_store_coverage', 's_sales_velocity', 
    's2_sales_velocity', 'lag_1d', 'lag_7d', 'rolling_mean_7d', 'rolling_std_7d'
]
target = 'qty'

X = df[features]
y = df[target]

# 2. Instantiate XGBoost Regressor model
model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    random_state=42
)

# Train the model
model.fit(X, y)
print("Model training completed!")

# 3. Serialize model object into .pkl format
model_filename = "sales_forecast_model_v1.pkl"
with open(model_filename, "wb") as f:
    pickle.dump(model, f)
```
