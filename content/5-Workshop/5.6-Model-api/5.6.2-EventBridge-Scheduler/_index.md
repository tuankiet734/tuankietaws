---
title: "Pipeline Automation"
date: 2024-07-07
weight: 2
chapter: false
pre : " <b> 5.6.2. </b> "
---

### 5.6.2. Pipeline Automation via Amazon EventBridge & Daily Cron Job

To ensure that the forecasting model regularly updates predictions as daily retail sales volume shifts, we establish an automated daily prediction pipeline.

The automated routine:
1. Gathers all active store-sku combinations from the latest recorded day in the `final_daily` table.
2. Generates the forecast dates (next 7 days).
3. Hits the EC2 Orchestrator API endpoint to execute the inference and save forecasts in the `demand_forecasts` table of RDS PostgreSQL.

---

#### 1. Daily Batch Forecast Script (`daily_forecast_updater.py`):

This script queries the backend API in small batches to prevent server overload:

```python
import json
import urllib.request
import urllib.error
import datetime
import psycopg2

# Configuration credentials for RDS & Orchestrator API
DB_HOST = "fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "fashiondb"
DB_USER = "dbadmin"
DB_PASS = "Tung2004"

# EC2 Backend Orchestrator Endpoint
EC2_API_URL = "http://18.141.158.110/predict/forecast"

def get_active_store_skus():
    """Fetches the distinct active store_id and sku pairs on the latest day."""
    print("Connecting to RDS to get active store-sku combinations...")
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()
    
    # 1. Fetch latest recorded date in final_daily
    cur.execute("SELECT MAX(date) FROM final_daily;")
    latest_date = cur.fetchone()[0]
    print(f"Latest active date: {latest_date}")
    
    # 2. Get distinct combinations active on that date
    query = """
        SELECT DISTINCT store_id, sku 
        FROM final_daily
        WHERE date = %s;
    """
    cur.execute(query, (latest_date,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    print(f"Found {len(rows)} active store-sku combinations on {latest_date}.")
    return rows

def run_daily_forecast():
    try:
        store_skus = get_active_store_skus()
    except Exception as e:
        print(f"Error fetching store-SKUs: {e}")
        return
        
    if not store_skus:
        print("No active store-sku combinations found.")
        return
        
    # Determine forecast dates (next 7 days starting from tomorrow)
    today = datetime.date.today()
    forecast_dates = [str(today + datetime.timedelta(days=i)) for i in range(1, 8)]
    print(f"Generating forecast for dates: {forecast_dates}")
    
    # Pack payloads
    items = []
    for store_id, sku in store_skus:
        for date_str in forecast_dates:
            items.append({
                "store_id": str(store_id),
                "sku": sku,
                "date": date_str
            })
            
    # Execute batch REST requests
    batch_size = 10
    total_items = len(items)
    print(f"Total forecast requests: {total_items}. Processing in batches of {batch_size}...")
    
    success_count = 0
    for i in range(0, total_items, batch_size):
        batch = items[i:i+batch_size]
        payload = {"items": batch}
        
        req = urllib.request.Request(
            EC2_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                res_body = response.read().decode('utf-8')
                res_json = json.loads(res_body)
                if res_json.get("status") == "success":
                    success_count += len(batch)
                    print(f"Batch {i//batch_size + 1} processed successfully. ({success_count}/{total_items})")
                else:
                    print(f"Batch {i//batch_size + 1} failed: {res_json.get('message')}")
        except urllib.error.HTTPError as he:
            print(f"HTTP Error on batch {i//batch_size + 1}: {he.code} - {he.read().decode('utf-8')}")
        except Exception as e:
            print(f"Error on batch {i//batch_size + 1}: {e}")
            
    print(f"\nCompleted! Successfully triggered forecasting for {success_count}/{total_items} items.")

if __name__ == "__main__":
    run_daily_forecast()
```

---

#### 2. Automation Configuration Options:

The daily batch pipeline can be automated using one of the following setups:

##### Option 1: AWS Lambda + Amazon EventBridge Scheduler (Serverless Cloud Setup)
1. Wrap the `daily_forecast_updater.py` code into an AWS Lambda function named `DailyForecastTrigger`.
2. Open **Amazon EventBridge Console** -> **Schedules**.
3. Create a new schedule:
   * **Schedule type:** Recurring schedule.
   * **Schedule pattern:** Cron-based schedule (e.g., `cron(0 1 * * ? *)` daily at 1:00 AM UTC).
   * **Target:** Choose **AWS Lambda** and associate it with the `DailyForecastTrigger` function.

##### Option 2: Linux Crontab on EC2 Server (Cost-effective Development Setup)
1. Log in to the backend EC2 server instance (`18.141.158.110`) via SSH.
2. Upload `daily_forecast_updater.py` to the server root.
3. Edit the server crontab:
   ```bash
   crontab -e
   ```
4. Append the cron rule to run at 2:00 AM daily:
   ```bash
   0 2 * * * /usr/bin/python3 /home/ubuntu/daily_forecast_updater.py >> /home/ubuntu/daily_forecast.log 2>&1
   ```

---

#### Verification on Amazon EventBridge:

![EventBridge Rule](/images/5-Workshop/5.6-Model-api/eventbridge-schedule.png)

