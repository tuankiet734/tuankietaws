---
title: "Kịch bản huấn luyện mô hình"
date: 2024-07-07
weight: 2
chapter: false
pre: " <b> 5.4.2. </b> "
---

### 5.4.2. Kịch bản Huấn luyện Mô hình dự báo (Python ML Script)

Mã nguồn Python chạy trên máy chủ thực hiện việc kết nối tới `training-db`, trích xuất bảng đặc trưng `final_daily`, tiền xử lý dữ liệu và huấn luyện mô hình dự báo sử dụng thuật toán **XGBoost Regressor** mạnh mẽ.

##### Phân đoạn mã nguồn xử lý cốt lõi:
```python
import pandas as pd
import xgboost as xgb
from sqlalchemy import create_engine
import pickle
import boto3

# 1. Kết nối cơ sở dữ liệu huấn luyện để lấy dữ liệu đặc trưng
db_url = "postgresql+psycopg2://dbadmin:Tung2004@training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com:5432/fashiondb"
engine = create_engine(db_url)
df = pd.read_sql("SELECT * FROM final_daily", engine)

# Sắp xếp và tiền xử lý dữ liệu đặc trưng
df = df.sort_values(by=['store_id', 'sku', 'date'])
features = [
    'avg_usd_price', 'total_discount_avg', 'total_lifespan', 's_total_lifespan',
    'sku_store_coverage', 'product_store_coverage', 's_sales_velocity', 
    's2_sales_velocity', 'lag_1d', 'lag_7d', 'rolling_mean_7d', 'rolling_std_7d'
]
target = 'qty'

X = df[features]
y = df[target]

# 2. Định nghĩa mô hình XGBoost cho bài toán hồi quy (Regression)
model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    random_state=42
)

# Tiến hành huấn luyện mô hình
model.fit(X, y)
print("Huấn luyện mô hình thành công!")

# 3. Đóng gói mô hình dưới dạng file serialize .pkl
model_filename = "sales_forecast_model_v1.pkl"
with open(model_filename, "wb") as f:
    pickle.dump(model, f)
```
