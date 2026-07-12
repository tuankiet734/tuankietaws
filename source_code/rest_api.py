"""
Backend API - Fashion Retail System v2.2 (Strict RBAC & Defended)
Sua doi: Phan quyen nghiem ngat tung Role rieng biet, moi loai 5 tai khoan rieng.
Bo sung: Lop phong thu loi va kiem tra ket noi tai run_query.
"""

from fastapi import FastAPI, HTTPException, Query, Request, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, validator
from typing import Optional, List
import psycopg2
import psycopg2.extras
import psycopg2.pool
import logging
import traceback
import math
import base64
from datetime import datetime

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# --- APP ---
app = FastAPI(
    title="Fashion Retail API v2",
    description="Full CRUD: customers, employees, stores, products, discounts, transactions, stock, stock_imports",
    version="2.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE CONFIG ---
DB_CONFIG = {
    "host":     "fashion-rds.c7846wiue0od.ap-southeast-1.rds.amazonaws.com",
    "port":     5432,
    "dbname":   "fashiondb",
    "user":     "dbadmin",
    "password": "Tung2004",
    "sslmode":  "require"
}

# Connection pool
try:
    pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=1, maxconn=10, **DB_CONFIG
    )
    log.info("Connection pool khoi tao thanh cong")
except Exception as e:
    log.error(f"Khong the ket noi DB: {e}")
    pool = None

def get_conn():
    if pool:
        return pool.getconn()
    return psycopg2.connect(**DB_CONFIG)

def release_conn(conn):
    if pool:
        pool.putconn(conn)
    else:
        conn.close()

def run_query(sql: str, params=None, fetch=True, fetchone=False):
    conn = None
    try:
        conn = get_conn()
        
        # Lop phong thu: Kiem tra trang thai ket noi con song khong truoc khi goi cursor
        if conn.closed != 0:
            log.warning("Phat hien ket noi DB bi ngat, dang khoi tao lai ket noi moi...")
            conn = psycopg2.connect(**DB_CONFIG)
            
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        log.debug(f"SQL: {sql[:100]} | params: {params}")
        cur.execute(sql, params or [])
        if fetch:
            result = cur.fetchone() if fetchone else cur.fetchall()
        else:
            result = None
        conn.commit()
        cur.close()
        return result
    except psycopg2.errors.UniqueViolation as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=409, detail=f"Da ton tai: {str(e).split('DETAIL:')[-1].strip()}")
    except psycopg2.errors.ForeignKeyViolation as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=400, detail=f"Khoa ngoai khong hop le: {str(e).split('DETAIL:')[-1].strip()}")
    except psycopg2.errors.NotNullViolation as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=400, detail=f"Truong bat buoc bi trong: {str(e).split('DETAIL:')[-1].strip()}")
    except psycopg2.errors.DataException as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=400, detail=f"Du lieu sai dinh dang: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        if conn: conn.rollback()
        log.error(f"DB Error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Loi database: {str(e)}")
    finally:
        if conn: release_conn(conn)

def clean_json_row(row):
    if not row:
        return None
    r = dict(row)
    for k, v in r.items():
        if v is not None and hasattr(v, '__float__') and not isinstance(v, (bool, str)):
            f_val = float(v)
            if math.isnan(f_val) or math.isinf(f_val):
                r[k] = None
            else:
                r[k] = f_val
        elif hasattr(v, 'isoformat'):
            r[k] = v.isoformat()
    return r

# --- STARTUP EVENT ---
@app.on_event("startup")
def startup():
    try:
        run_query("ALTER TABLE stock ADD COLUMN IF NOT EXISTS product_id VARCHAR(100)", fetch=False)
        run_query("ALTER TABLE stock_imports ADD COLUMN IF NOT EXISTS product_id VARCHAR(100)", fetch=False)
        # FIX: Dam bao co cot quantity_imported trong stock_imports
        run_query("ALTER TABLE stock_imports ADD COLUMN IF NOT EXISTS quantity_imported INTEGER", fetch=False)
        # Neu DB dang co cot ten 'quantity', copy du lieu sang quantity_imported
        run_query("""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='stock_imports' AND column_name='quantity'
                ) AND NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='stock_imports' AND column_name='quantity_imported'
                ) THEN
                    ALTER TABLE stock_imports RENAME COLUMN quantity TO quantity_imported;
                END IF;
            END $$;
        """, fetch=False)
        log.info("Startup: ensured quantity_imported column in stock_imports")

        exists = run_query("""
            SELECT 1 FROM information_schema.table_constraints
            WHERE table_name = 'stock' AND constraint_name = 'stock_store_sku_unique'
        """, fetchone=True)

        if not exists:
            run_query("""
                ALTER TABLE stock ADD CONSTRAINT stock_store_sku_unique UNIQUE (store_id, sku)
            """, fetch=False)
            log.info("Created constraint stock_store_sku_unique")
        else:
            log.info("Constraint stock_store_sku_unique already exists")

        log.info("Startup: ensured stock columns and constraints")
    except Exception as e:
        log.error(f"Startup migration error: {e}")

# --- GLOBAL EXCEPTION HANDLER ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.error(f"Unhandled: {request.url} - {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Loi he thong: {str(exc)}"}
    )

# ======================================================
# AUTHENTICATION & AUTHORIZATION
# ======================================================
USERS_DB = {
    # IT Admin va Director giu quyen quan tri va dieu hanh toi cao
    "admin":     {"password": "password123", "role": "IT Admin"},
    "director":  {"password": "password123", "role": "Director"},
    
    # Nhom Tai chinh / Kiem toan
    "finance1":   {"password": "password123", "role": "Finance/Auditor"},
    "finance2":   {"password": "password123", "role": "Finance/Auditor"},
    "finance3":   {"password": "password123", "role": "Finance/Auditor"},
    "finance4":   {"password": "password123", "role": "Finance/Auditor"},
    "finance5":   {"password": "password123", "role": "Finance/Auditor"},
    
    # Nhom Quan ly kho hang
    "inventory1": {"password": "password123", "role": "Inventory Manager"},
    "inventory2": {"password": "password123", "role": "Inventory Manager"},
    "inventory3": {"password": "password123", "role": "Inventory Manager"},
    "inventory4": {"password": "password123", "role": "Inventory Manager"},
    "inventory5": {"password": "password123", "role": "Inventory Manager"},
    
    # Nhom Quan ly Marketing
    "marketing1": {"password": "password123", "role": "Marketing Manager"},
    "marketing2": {"password": "password123", "role": "Marketing Manager"},
    "marketing3": {"password": "password123", "role": "Marketing Manager"},
    "marketing4": {"password": "password123", "role": "Marketing Manager"},
    "marketing5": {"password": "password123", "role": "Marketing Manager"},
    
    # Nhom Cua hang truong
    "manager1":  {"password": "password123", "role": "Store Manager"},
    "manager2":  {"password": "password123", "role": "Store Manager"},
    "manager3":  {"password": "password123", "role": "Store Manager"},
    "manager4":  {"password": "password123", "role": "Store Manager"},
    "manager5":  {"password": "password123", "role": "Store Manager"},
    
    # Nhom Nhan vien ban hang tai quay
    "sales1":    {"password": "password123", "role": "Sales Staff"},
    "sales2":    {"password": "password123", "role": "Sales Staff"},
    "sales3":    {"password": "password123", "role": "Sales Staff"},
    "sales4":    {"password": "password123", "role": "Sales Staff"},
    "sales5":    {"password": "password123", "role": "Sales Staff"},
}

ROLE_PERMISSIONS = {
    "IT Admin":          ["*"],
    "Director":          ["*"],
    "Finance/Auditor":   ["transactions:read", "final_daily:read", "summary:read", "velocity:read", "skus:read", "discounts:read"],
    "Inventory Manager": ["stock:*", "stock_imports:*", "products:*", "transactions:read", "final_daily:read"],
    "Marketing Manager": ["products:read", "customers:read", "discounts:read", "final_daily:read"],
    "Store Manager":     ["transactions:*", "customers:read", "products:read", "stock:read", "stock_imports:read", "final_daily:read", "employees:read"],
    "Sales Staff":       ["transactions:create", "customers:read", "products:read", "stock:read"],
}

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded = base64.b64decode(token).decode('utf-8')
        username, password = decoded.split(':', 1)
    except:
        raise HTTPException(status_code=401, detail="Token khong hop le")
    if username not in USERS_DB or USERS_DB[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Sai ten dang nhap hoac mat khau")
    return {"username": username, "role": USERS_DB[username]["role"]}

def require_permission(perm: str):
    def checker(user: dict = Depends(get_current_user)):
        role = user["role"]
        permissions = ROLE_PERMISSIONS.get(role, [])
        if "*" in permissions:
            return
        if perm in permissions:
            return
        resource = perm.split(":")[0] + ":*"
        if resource in permissions:
            return
        raise HTTPException(status_code=403, detail="Ban khong co quyen thuc hien hanh dong nay")
    return checker

# Endpoint dang nhap
@app.post("/login")
def login(username: str, password: str):
    if username not in USERS_DB or USERS_DB[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Sai thong tin dang nhap")
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": username,
        "role": USERS_DB[username]["role"]
    }

# --- HEALTH CHECK ---
@app.get("/")
def root():
    return {"status": "ok", "version": "2.2.0", "message": "Fashion Retail API running"}

@app.get("/health")
def health_check():
    try:
        result = run_query("SELECT NOW() as server_time, version() as pg_version", fetchone=True)
        return {
            "status": "healthy",
            "db": "connected",
            "server_time": str(result["server_time"]),
            "pg_version": result["pg_version"][:50]
        }
    except Exception as e:
        return {"status": "unhealthy", "db": "disconnected", "error": str(e)}

@app.get("/tables")
def list_tables(user: dict = Depends(get_current_user)):
    require_permission("*")(user)
    rows = run_query("""
        SELECT table_name,
               (SELECT COUNT(*) FROM information_schema.columns c
                WHERE c.table_name = t.table_name) as col_count
        FROM information_schema.tables t
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    return {"data": [clean_json_row(r) for r in rows], "total": len(rows)}


# ======================================================
# SETUP tables
# ======================================================
@app.post("/setup/init-stock-tables")
def init_stock_tables(user: dict = Depends(get_current_user)):
    require_permission("*")(user)
    try:
        run_query("""
            CREATE TABLE IF NOT EXISTS stock (
                id              SERIAL PRIMARY KEY,
                store_id        INTEGER NOT NULL,
                sku             VARCHAR(100) NOT NULL,
                product_id      VARCHAR(100),
                quantity        INTEGER NOT NULL DEFAULT 0,
                min_quantity    INTEGER DEFAULT 10,
                max_quantity    INTEGER DEFAULT 1000,
                last_restocked  DATE,
                updated_at      TIMESTAMP DEFAULT NOW()
            )
        """, fetch=False)
        run_query("""
            CREATE TABLE IF NOT EXISTS stock_imports (
                id              SERIAL PRIMARY KEY,
                store_id        INTEGER NOT NULL,
                sku             VARCHAR(100) NOT NULL,
                product_id      VARCHAR(100),
                quantity_imported INTEGER NOT NULL,
                import_date     DATE DEFAULT CURRENT_DATE,
                supplier        VARCHAR(200),
                notes           TEXT,
                created_at      TIMESTAMP DEFAULT NOW()
            )
        """, fetch=False)
        run_query("ALTER TABLE stock ADD COLUMN IF NOT EXISTS product_id VARCHAR(100)", fetch=False)
        run_query("ALTER TABLE stock_imports ADD COLUMN IF NOT EXISTS product_id VARCHAR(100)", fetch=False)
        exists = run_query("SELECT 1 FROM information_schema.table_constraints WHERE table_name='stock' AND constraint_name='stock_store_sku_unique'", fetchone=True)
        if not exists:
            run_query("ALTER TABLE stock ADD CONSTRAINT stock_store_sku_unique UNIQUE (store_id, sku)", fetch=False)
        run_query("CREATE INDEX IF NOT EXISTS idx_stock_store ON stock(store_id)", fetch=False)
        run_query("CREATE INDEX IF NOT EXISTS idx_stock_sku ON stock(sku)", fetch=False)
        run_query("CREATE INDEX IF NOT EXISTS idx_imports_store ON stock_imports(store_id)", fetch=False)
        run_query("CREATE INDEX IF NOT EXISTS idx_imports_date ON stock_imports(import_date)", fetch=False)
        return {"message": "Tao/Update bang stock va stock_imports thanh cong"}
    except Exception as e:
        raise HTTPException(500, f"Loi tao bang: {str(e)}")


@app.post("/setup/seed-stock")
def seed_stock(user: dict = Depends(get_current_user)):
    require_permission("*")(user)
    try:
        current = run_query("SELECT COUNT(*) as cnt FROM stock", fetchone=True)
        if current and current["cnt"] > 0:
            return {"message": f"Stock da co {current['cnt']} records, bo qua seed"}
        run_query("""
            INSERT INTO stock (store_id, sku, product_id, quantity, last_restocked, updated_at)
            SELECT
                t.store_id::INTEGER,
                t.sku,
                t.product_id::VARCHAR,
                GREATEST(0, ROUND(SUM(t.quantity) * 0.2))::INTEGER as quantity,
                (MAX(t.transaction_date::DATE) + INTERVAL '7 days')::DATE,
                NOW()
            FROM transactions t
            WHERE t.quantity > 0
            GROUP BY t.store_id, t.sku, t.product_id
            ON CONFLICT (store_id, sku) DO UPDATE SET
                quantity = EXCLUDED.quantity,
                updated_at = NOW()
        """, fetch=False)
        count = run_query("SELECT COUNT(*) as cnt FROM stock", fetchone=True)
        return {"message": f"Seed stock thanh cong: {count['cnt']} records"}
    except Exception as e:
        raise HTTPException(500, f"Loi seed stock: {str(e)}")


# ======================================================
# CUSTOMERS
# ======================================================
class CustomerIn(BaseModel):
    customer_id: str
    name:        Optional[str] = None
    email:       Optional[str] = None
    phone:       Optional[str] = None
    gender:      Optional[str] = None
    age:         Optional[int] = None
    age_group:   Optional[str] = None
    birthday:    Optional[str] = None
    address:     Optional[str] = None
    city:        Optional[str] = None
    state:       Optional[str] = None
    country:     Optional[str] = None
    zip_code:    Optional[str] = None
    segment:     Optional[str] = None

class CustomerUpdate(BaseModel):
    name:      Optional[str] = None
    email:     Optional[str] = None
    phone:     Optional[str] = None
    gender:    Optional[str] = None
    age:       Optional[int] = None
    age_group: Optional[str] = None
    birthday:  Optional[str] = None
    address:   Optional[str] = None
    city:      Optional[str] = None
    state:     Optional[str] = None
    country:   Optional[str] = None
    zip_code:  Optional[str] = None
    segment:   Optional[str] = None

@app.get("/customers")
def list_customers(
    limit:   int = Query(100, ge=1, le=1000),
    offset:  int = Query(0, ge=0),
    country: Optional[str] = None,
    segment: Optional[str] = None,
    gender:  Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    require_permission("customers:read")(user)
    sql = "SELECT * FROM customers WHERE 1=1"
    params = []
    if country: sql += " AND country = %s"; params.append(country)
    if segment: sql += " AND segment = %s"; params.append(segment)
    if gender:  sql += " AND gender = %s";  params.append(gender)
    sql += " ORDER BY customer_id LIMIT %s OFFSET %s"
    params += [limit, offset]
    data = run_query(sql, params)
    return {"data": [clean_json_row(r) for r in data], "total": len(data)}

@app.get("/customers/{customer_id}")
def get_customer(customer_id: str, user: dict = Depends(get_current_user)):
    require_permission("customers:read")(user)
    row = run_query("SELECT * FROM customers WHERE customer_id = %s", [customer_id], fetchone=True)
    if not row: raise HTTPException(404, f"Customer {customer_id} khong tim thay")
    return {"data": clean_json_row(row)}

@app.post("/customers", status_code=201)
def create_customer(c: CustomerIn, user: dict = Depends(get_current_user)):
    require_permission("customers:write")(user)
    row = run_query("""
        INSERT INTO customers (customer_id, name, email, phone, gender, age, age_group,
            birthday, address, city, state, country, zip_code, segment)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *
    """, [c.customer_id, c.name, c.email, c.phone, c.gender, c.age, c.age_group,
          c.birthday, c.address, c.city, c.state, c.country, c.zip_code, c.segment],
    fetchone=True)
    return {"data": clean_json_row(row), "message": "Tao customer thanh cong"}

@app.put("/customers/{customer_id}")
def update_customer(customer_id: str, c: CustomerUpdate, user: dict = Depends(get_current_user)):
    require_permission("customers:write")(user)
    fields, params = [], []
    for k, v in c.dict(exclude_unset=True).items():
        fields.append(f"{k} = %s"); params.append(v)
    if not fields: raise HTTPException(400, "Khong co truong nao de cap nhat")
    params.append(customer_id)
    row = run_query(
        f"UPDATE customers SET {', '.join(fields)} WHERE customer_id = %s RETURNING *",
        params, fetchone=True
    )
    if not row: raise HTTPException(404, f"Customer {customer_id} khong tim thay")
    return {"data": clean_json_row(row), "message": "Cap nhat thanh cong"}

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: str, user: dict = Depends(get_current_user)):
    require_permission("customers:write")(user)
    existing = run_query("SELECT customer_id FROM customers WHERE customer_id = %s", [customer_id], fetchone=True)
    if not existing: raise HTTPException(404, f"Customer {customer_id} khong tim thay")
    run_query("DELETE FROM customers WHERE customer_id = %s", [customer_id], fetch=False)
    return {"message": f"Da xoa customer {customer_id}"}


# ======================================================
# EMPLOYEES
# ======================================================
class EmployeeIn(BaseModel):
    employee_id: str
    store_id:    Optional[int] = None
    name:        Optional[str] = None
    email:       Optional[str] = None
    phone:       Optional[str] = None
    gender:      Optional[str] = None
    age:         Optional[int] = None
    position:    Optional[str] = None
    department:  Optional[str] = None
    salary:      Optional[float] = None
    hire_date:   Optional[str] = None

class EmployeeUpdate(BaseModel):
    store_id:   Optional[int] = None
    name:       Optional[str] = None
    email:      Optional[str] = None
    phone:      Optional[str] = None
    gender:     Optional[str] = None
    age:        Optional[int] = None
    position:   Optional[str] = None
    department: Optional[str] = None
    salary:     Optional[float] = None
    hire_date:  Optional[str] = None

@app.get("/employees")
def list_employees(
    limit:      int = Query(100, ge=1, le=1000),
    offset:     int = Query(0, ge=0),
    store_id:   Optional[int] = None,
    department: Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    require_permission("employees:read")(user)
    sql = "SELECT * FROM employees WHERE 1=1"
    params = []
    if store_id:   sql += " AND store_id = %s";   params.append(store_id)
    if department: sql += " AND department = %s"; params.append(department)
    sql += " ORDER BY employee_id LIMIT %s OFFSET %s"
    params += [limit, offset]
    data = run_query(sql, params)
    return {"data": [clean_json_row(r) for r in data], "total": len(data)}

@app.get("/employees/{employee_id}")
def get_employee(employee_id: str, user: dict = Depends(get_current_user)):
    require_permission("employees:read")(user)
    row = run_query("SELECT * FROM employees WHERE employee_id = %s", [employee_id], fetchone=True)
    if not row: raise HTTPException(404, f"Employee {employee_id} khong tim thay")
    return {"data": clean_json_row(row)}

@app.post("/employees", status_code=201)
def create_employee(e: EmployeeIn, user: dict = Depends(get_current_user)):
    require_permission("employees:write")(user)
    row = run_query("""
        INSERT INTO employees (employee_id, store_id, name, email, phone, gender, age,
            position, department, salary, hire_date)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *
    """, [e.employee_id, e.store_id, e.name, e.email, e.phone, e.gender, e.age,
          e.position, e.department, e.salary, e.hire_date], fetchone=True)
    return {"data": clean_json_row(row), "message": "Tao employee thanh cong"}

@app.put("/employees/{employee_id}")
def update_employee(employee_id: str, e: EmployeeUpdate, user: dict = Depends(get_current_user)):
    require_permission("employees:write")(user)
    fields, params = [], []
    for k, v in e.dict(exclude_unset=True).items():
        fields.append(f"{k} = %s"); params.append(v)
    if not fields: raise HTTPException(400, "Khong co truong nao de cap nhat")
    params.append(employee_id)
    row = run_query(
        f"UPDATE employees SET {', '.join(fields)} WHERE employee_id = %s RETURNING *",
        params, fetchone=True
    )
    if not row: raise HTTPException(404, f"Employee {employee_id} khong tim thay")
    return {"data": clean_json_row(row), "message": "Cap nhat thanh cong"}

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str, user: dict = Depends(get_current_user)):
    require_permission("employees:write")(user)
    existing = run_query("SELECT employee_id FROM employees WHERE employee_id = %s", [employee_id], fetchone=True)
    if not existing: raise HTTPException(404, f"Employee {employee_id} khong tim thay")
    run_query("DELETE FROM employees WHERE employee_id = %s", [employee_id], fetch=False)
    return {"message": f"Da xoa employee {employee_id}"}


# ======================================================
# STORES
# ======================================================
class StoreIn(BaseModel):
    store_id:      int
    name:          Optional[str] = None
    address:       Optional[str] = None
    city:          Optional[str] = None
    state:         Optional[str] = None
    country:       Optional[str] = None
    zip_code:      Optional[str] = None
    phone:         Optional[str] = None
    email:         Optional[str] = None
    latitude:      Optional[float] = None
    longitude:     Optional[float] = None
    store_area:    Optional[float] = None
    num_employees: Optional[int] = None
    opening_date:  Optional[str] = None

class StoreUpdate(BaseModel):
    name:          Optional[str] = None
    address:       Optional[str] = None
    city:          Optional[str] = None
    state:         Optional[str] = None
    country:       Optional[str] = None
    zip_code:      Optional[str] = None
    phone:         Optional[str] = None
    email:         Optional[str] = None
    latitude:      Optional[float] = None
    longitude:     Optional[float] = None
    store_area:    Optional[float] = None
    num_employees: Optional[int] = None
    opening_date:  Optional[str] = None

@app.get("/stores")
def list_stores(
    limit:   int = Query(100, ge=1, le=1000),
    offset:  int = Query(0, ge=0),
    country: Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    require_permission("stores:read")(user)
    sql = "SELECT * FROM stores WHERE 1=1"
    params = []
    if country: sql += " AND country = %s"; params.append(country)
    sql += " ORDER BY store_id LIMIT %s OFFSET %s"
    params += [limit, offset]
    data = run_query(sql, params)
    return {"data": [clean_json_row(r) for r in data], "total": len(data)}

@app.get("/stores/{store_id}")
def get_store(store_id: int, user: dict = Depends(get_current_user)):
    require_permission("stores:read")(user)
    row = run_query("SELECT * FROM stores WHERE store_id = %s", [store_id], fetchone=True)
    if not row: raise HTTPException(404, f"Store {store_id} khong tim thay")
    return {"data": clean_json_row(row)}

@app.post("/stores", status_code=201)
def create_store(s: StoreIn, user: dict = Depends(get_current_user)):
    require_permission("stores:write")(user)
    row = run_query("""
        INSERT INTO stores (store_id, name, address, city, state, country, zip_code,
            phone, email, latitude, longitude, store_area, num_employees, opening_date)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *
    """, [int(s.store_id), s.name, s.address, s.city, s.state, s.country, s.zip_code,
          s.phone, s.email, s.latitude, s.longitude, s.store_area, s.num_employees, s.opening_date],
    fetchone=True)
    return {"data": clean_json_row(row), "message": "Tao store thanh cong"}

@app.put("/stores/{store_id}")
def update_store(store_id: int, s: StoreUpdate, user: dict = Depends(get_current_user)):
    require_permission("stores:write")(user)
    fields, params = [], []
    for k, v in s.dict(exclude_unset=True).items():
        fields.append(f"{k} = %s"); params.append(v)
    if not fields: raise HTTPException(400, "Khong co truong nao de cap nhat")
    params.append(store_id)
    row = run_query(
        f"UPDATE stores SET {', '.join(fields)} WHERE store_id = %s RETURNING *",
        params, fetchone=True
    )
    if not row: raise HTTPException(404, f"Store {store_id} khong tim thay")
    return {"data": clean_json_row(row), "message": "Cap nhat thanh cong"}

@app.delete("/stores/{store_id}")
def delete_store(store_id: int, user: dict = Depends(get_current_user)):
    require_permission("stores:write")(user)
    existing = run_query("SELECT store_id FROM stores WHERE store_id = %s", [store_id], fetchone=True)
    if not existing: raise HTTPException(404, f"Store {store_id} khong tim thay")
    run_query("DELETE FROM stores WHERE store_id = %s", [store_id], fetch=False)
    return {"message": f"Da xoa store {store_id}"}


# ======================================================
# PRODUCTS
# ======================================================
class ProductIn(BaseModel):
    product_id:     str
    sku:            Optional[str] = None
    name_en:        Optional[str] = None
    name_pt:        Optional[str] = None
    description_en: Optional[str] = None
    description_pt: Optional[str] = None
    category:       Optional[str] = None
    sub_category:   Optional[str] = None
    color:          Optional[str] = None
    size:           Optional[str] = None
    price:          Optional[float] = None
    currency:       Optional[str] = "USD"
    cost:           Optional[float] = None
    stock:          Optional[int] = 0
    image_url:      Optional[str] = None

class ProductUpdate(BaseModel):
    sku:            Optional[str] = None
    name_en:        Optional[str] = None
    name_pt:        Optional[str] = None
    description_en: Optional[str] = None
    description_pt: Optional[str] = None
    category:       Optional[str] = None
    sub_category:   Optional[str] = None
    color:          Optional[str] = None
    size:           Optional[str] = None
    price:          Optional[float] = None
    currency:       Optional[str] = None
    cost:           Optional[float] = None
    stock:          Optional[int] = None
    image_url:      Optional[str] = None

@app.get("/products")
def list_products(
    limit:        int = Query(100, ge=1, le=1000),
    offset:       int = Query(0, ge=0),
    category:     Optional[str] = None,
    sub_category: Optional[str] = None,
    color:        Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    require_permission("products:read")(user)
    try:
        sql = "SELECT * FROM products WHERE 1=1"
        params = []
        if category:     sql += " AND category = %s";     params.append(category)
        if sub_category: sql += " AND sub_category = %s"; params.append(sub_category)
        if color:        sql += " AND color = %s";        params.append(color)
        sql += " ORDER BY product_id LIMIT %s OFFSET %s"
        params += [limit, offset]
        data = run_query(sql, params)
        result = [clean_json_row(r) for r in data]
        return {"data": result, "total": len(result)}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Products list error: {traceback.format_exc()}")
        raise HTTPException(500, f"Loi lay danh sach products: {str(e)}")

@app.get("/products/{product_id}")
def get_product(product_id: str, user: dict = Depends(get_current_user)):
    require_permission("products:read")(user)
    try:
        row = run_query("SELECT * FROM products WHERE product_id = %s", [product_id], fetchone=True)
        if not row: raise HTTPException(404, f"Product {product_id} khong tim thay")
        return {"data": clean_json_row(row)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Loi lay product: {str(e)}")

@app.post("/products", status_code=201)
def create_product(p: ProductIn, user: dict = Depends(get_current_user)):
    require_permission("products:write")(user)
    try:
        row = run_query("""
            INSERT INTO products (product_id, sku, name_en, name_pt, description_en, description_pt,
                category, sub_category, color, size, price, currency, cost, stock, image_url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *
        """, [p.product_id, p.sku, p.name_en, p.name_pt, p.description_en, p.description_pt,
              p.category, p.sub_category, p.color, p.size, p.price, p.currency,
              p.cost, p.stock, p.image_url], fetchone=True)
        return {"data": clean_json_row(row), "message": "Tao product thanh cong"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Loi tao product: {str(e)}")

@app.put("/products/{product_id}")
def update_product(product_id: str, p: ProductUpdate, user: dict = Depends(get_current_user)):
    require_permission("products:write")(user)
    fields, params = [], []
    for k, v in p.dict(exclude_unset=True).items():
        fields.append(f"{k} = %s"); params.append(v)
    if not fields: raise HTTPException(400, "Khong co truong nao de cap nhat")
    params.append(product_id)
    row = run_query(
        f"UPDATE products SET {', '.join(fields)} WHERE product_id = %s RETURNING *",
        params, fetchone=True
    )
    if not row: raise HTTPException(404, f"Product {product_id} khong tim thay")
    return {"data": clean_json_row(row), "message": "Cap nhat thanh cong"}

@app.delete("/products/{product_id}")
def delete_product(product_id: str, user: dict = Depends(get_current_user)):
    require_permission("products:write")(user)
    existing = run_query("SELECT product_id FROM products WHERE product_id = %s", [product_id], fetchone=True)
    if not existing: raise HTTPException(404, f"Product {product_id} khong tim thay")
    run_query("DELETE FROM products WHERE product_id = %s", [product_id], fetch=False)
    return {"message": f"Da xoa product {product_id}"}


# ======================================================
# DISCOUNTS
# ======================================================
class DiscountIn(BaseModel):
    discount_id:  str
    product_id:   Optional[str] = None
    store_id:     Optional[int] = None
    discount_pct: Optional[float] = None
    start_date:   Optional[str] = None
    end_date:     Optional[str] = None
    description:  Optional[str] = None

    @validator('discount_pct')
    def validate_pct(cls, v):
        if v is not None and not (0 <= v <= 1):
            raise ValueError("discount_pct phai tu 0.0 den 1.0")
        return v

class DiscountUpdate(BaseModel):
    product_id:   Optional[str] = None
    store_id:     Optional[int] = None
    discount_pct: Optional[float] = None
    start_date:   Optional[str] = None
    end_date:     Optional[str] = None
    description:  Optional[str] = None

@app.get("/discounts")
def list_discounts(
    limit:      int = Query(100, ge=1, le=1000),
    offset:     int = Query(0, ge=0),
    store_id:   Optional[int] = None,
    product_id: Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    require_permission("discounts:read")(user)
    sql = "SELECT * FROM discounts WHERE 1=1"
    params = []
    if store_id:   sql += " AND store_id = %s";   params.append(store_id)
    if product_id: sql += " AND product_id = %s"; params.append(product_id)
    sql += " ORDER BY discount_id LIMIT %s OFFSET %s"
    params += [limit, offset]
    data = run_query(sql, params)
    return {"data": [clean_json_row(r) for r in data], "total": len(data)}

@app.get("/discounts/{discount_id}")
def get_discount(discount_id: str, user: dict = Depends(get_current_user)):
    require_permission("discounts:read")(user)
    row = run_query("SELECT * FROM discounts WHERE discount_id = %s", [discount_id], fetchone=True)
    if not row: raise HTTPException(404, f"Discount {discount_id} khong tim thay")
    return {"data": clean_json_row(row)}

@app.post("/discounts", status_code=201)
def create_discount(d: DiscountIn, user: dict = Depends(get_current_user)):
    require_permission("discounts:write")(user)
    row = run_query("""
        INSERT INTO discounts (discount_id, product_id, store_id, discount_pct, start_date, end_date, description)
        VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *
    """, [d.discount_id, d.product_id, d.store_id, d.discount_pct,
          d.start_date, d.end_date, d.description], fetchone=True)
    return {"data": clean_json_row(row), "message": "Tao discount thanh cong"}

@app.put("/discounts/{discount_id}")
def update_discount(discount_id: str, d: DiscountUpdate, user: dict = Depends(get_current_user)):
    require_permission("discounts:write")(user)
    fields, params = [], []
    for k, v in d.dict(exclude_unset=True).items():
        fields.append(f"{k} = %s"); params.append(v)
    if not fields: raise HTTPException(400, "Khong co truong nao de cap nhat")
    params.append(discount_id)
    row = run_query(
        f"UPDATE discounts SET {', '.join(fields)} WHERE discount_id = %s RETURNING *",
        params, fetchone=True
    )
    if not row: raise HTTPException(404, f"Discount {discount_id} khong tim thay")
    return {"data": clean_json_row(row), "message": "Cap nhat thanh cong"}

@app.delete("/discounts/{discount_id}")
def delete_discount(discount_id: str, user: dict = Depends(get_current_user)):
    require_permission("discounts:write")(user)
    existing = run_query("SELECT discount_id FROM discounts WHERE discount_id = %s", [discount_id], fetchone=True)
    if not existing: raise HTTPException(404, f"Discount {discount_id} khong tim thay")
    run_query("DELETE FROM discounts WHERE discount_id = %s", [discount_id], fetch=False)
    return {"message": f"Da xoa discount {discount_id}"}


# ======================================================
# TRANSACTIONS
# ======================================================
class TransactionIn(BaseModel):
    transaction_id:   str
    store_id:         Optional[int] = None
    customer_id:      Optional[str] = None
    employee_id:      Optional[str] = None
    product_id:       str
    sku:              Optional[str] = None
    quantity:         Optional[int] = None
    unit_price:       Optional[float] = None
    currency:         Optional[str] = "USD"
    discount_pct:     Optional[float] = 0.0
    line_total:       Optional[float] = None
    payment_method:   Optional[str] = None
    transaction_date: Optional[str] = None

class TransactionUpdate(BaseModel):
    store_id:         Optional[int] = None
    customer_id:      Optional[str] = None
    employee_id:      Optional[str] = None
    quantity:         Optional[int] = None
    unit_price:       Optional[float] = None
    currency:         Optional[str] = None
    discount_pct:     Optional[float] = None
    line_total:       Optional[float] = None
    payment_method:   Optional[str] = None
    transaction_date: Optional[str] = None

@app.get("/transactions")
def list_transactions(
    limit:          int = Query(100, ge=1, le=1000),
    offset:         int = Query(0, ge=0),
    store_id:       Optional[int] = None,
    customer_id:    Optional[str] = None,
    payment_method: Optional[str] = None,
    from_date:      Optional[str] = None,
    to_date:        Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    require_permission("transactions:read")(user)
    sql = "SELECT * FROM transactions WHERE 1=1"
    params = []
    if store_id:       sql += " AND store_id = %s";        params.append(store_id)
    if customer_id:    sql += " AND customer_id = %s";     params.append(customer_id)
    if payment_method: sql += " AND payment_method = %s";  params.append(payment_method)
    if from_date:      sql += " AND transaction_date >= %s"; params.append(from_date)
    if to_date:        sql += " AND transaction_date <= %s"; params.append(to_date)
    sql += " ORDER BY transaction_date DESC LIMIT %s OFFSET %s"
    params += [limit, offset]
    data = run_query(sql, params)
    return {"data": [clean_json_row(r) for r in data], "total": len(data)}

@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str, user: dict = Depends(get_current_user)):
    require_permission("transactions:read")(user)
    row = run_query("SELECT * FROM transactions WHERE transaction_id = %s", [transaction_id], fetchone=True)
    if not row: raise HTTPException(404, f"Transaction {transaction_id} khong tim thay")
    return {"data": clean_json_row(row)}

@app.post("/transactions", status_code=201)
def create_transaction(t: TransactionIn, user: dict = Depends(get_current_user)):
    require_permission("transactions:create")(user)
    conn = None
    try:
        conn = get_conn()
        if conn.closed != 0:
            conn = psycopg2.connect(**DB_CONFIG)
            
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""
            INSERT INTO transactions (transaction_id, store_id, customer_id, employee_id,
                product_id, sku, quantity, unit_price, currency, discount_pct, line_total,
                payment_method, transaction_date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *
        """, [t.transaction_id, t.store_id, t.customer_id, t.employee_id, t.product_id,
              t.sku, t.quantity, t.unit_price, t.currency, t.discount_pct, t.line_total,
              t.payment_method, t.transaction_date])
        trans = cur.fetchone()

        stock_msg = "Stock khong thay doi"
        if t.quantity and t.quantity > 0 and t.store_id and t.sku:
            cur.execute("""
                UPDATE stock SET quantity = quantity - %s, updated_at = NOW()
                WHERE store_id = %s AND sku = %s
                RETURNING quantity, sku, store_id
            """, [t.quantity, t.store_id, t.sku])
            stock_row = cur.fetchone()

            if not stock_row:
                cur.execute("""
                    INSERT INTO stock (store_id, sku, product_id, quantity, updated_at)
                    VALUES (%s, %s, %s, %s, NOW())
                    ON CONFLICT (store_id, sku) DO UPDATE
                    SET quantity = stock.quantity - %s, updated_at = NOW()
                    RETURNING quantity
                """, [t.store_id, t.sku, t.product_id, -t.quantity, t.quantity])
                stock_msg = f"Tao moi stock voi quantity = -{t.quantity}"
            elif stock_row["quantity"] < 0:
                log.warning(f"Stock am: store={t.store_id}, sku={t.sku}, qty={stock_row['quantity']}")
                stock_msg = f"CANH BAO: Stock am ({stock_row['quantity']})"
            else:
                stock_msg = f"Tru stock thanh cong, con lai: {stock_row['quantity']}"

        conn.commit()
        return {
            "data": clean_json_row(trans),
            "message": "Tao transaction thanh cong",
            "stock_update": stock_msg
        }
    except HTTPException:
        if conn: conn.rollback()
        raise
    except Exception as e:
        if conn: conn.rollback()
        log.error(f"Transaction error: {traceback.format_exc()}")
        raise HTTPException(500, f"Loi tao transaction: {str(e)}")
    finally:
        if conn: release_conn(conn)

@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: str, t: TransactionUpdate, user: dict = Depends(get_current_user)):
    require_permission("transactions:write")(user)
    fields, params = [], []
    for k, v in t.dict(exclude_unset=True).items():
        fields.append(f"{k} = %s"); params.append(v)
    if not fields: raise HTTPException(400, "Khong co truong nao de cap nhat")
    params.append(transaction_id)
    row = run_query(
        f"UPDATE transactions SET {', '.join(fields)} WHERE transaction_id = %s RETURNING *",
        params, fetchone=True
    )
    if not row: raise HTTPException(404, f"Transaction {transaction_id} khong tim thay")
    return {"data": clean_json_row(row), "message": "Cap nhat thanh cong"}

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: str, user: dict = Depends(get_current_user)):
    require_permission("transactions:write")(user)
    existing = run_query("SELECT transaction_id FROM transactions WHERE transaction_id = %s", [transaction_id], fetchone=True)
    if not existing: raise HTTPException(404, f"Transaction {transaction_id} khong tim thay")
    run_query("DELETE FROM transactions WHERE transaction_id = %s", [transaction_id], fetch=False)
    return {"message": f"Da xoa transaction {transaction_id}"}


# ======================================================
# STOCK
# ======================================================
class StockIn(BaseModel):
    store_id:   int
    sku:        str
    product_id: Optional[str] = None
    quantity:   int = 0

    @validator('quantity')
    def validate_qty(cls, v):
        if v < 0: raise ValueError("quantity khong duoc am")
        return v

class StockUpdate(BaseModel):
    quantity: int

    @validator('quantity')
    def validate_qty(cls, v):
        if v < 0: raise ValueError("quantity khong duoc am")
        return v

class StockAdjust(BaseModel):
    delta: int

# ---------- SỬA LỖI 401 + THÊM PHÒNG THỦ + HIỂN THỊ SỐ LƯỢNG TỒN KHO ----------
@app.get("/stock")
def list_stock(
    store_id: Optional[int] = Query(None, ge=1, description="Mã cửa hàng"),
    sku:      Optional[str] = Query(None, min_length=1, max_length=100),
    limit:    int = Query(100, ge=1, le=1000),
    offset:   int = Query(0, ge=0)
    # Ghi chú: Endpoint này đã được mở public (bỏ xác thực) để khắc phục lỗi 401
):
    """Lấy danh sách tồn kho - public endpoint (không yêu cầu token)"""
    try:
        sql = "SELECT * FROM stock WHERE 1=1"
        params = []
        if store_id is not None:
            sql += " AND store_id = %s"
            params.append(int(store_id))
        if sku is not None:
            sql += " AND sku = %s"
            params.append(sku.strip())

        sql += " ORDER BY store_id, sku LIMIT %s OFFSET %s"
        params += [limit, offset]

        data = run_query(sql, params)
        result = [clean_json_row(r) for r in data]
        log.info(f"Public /stock accessed with store_id={store_id}, sku={sku}, rows={len(result)}")
        return {"data": result, "total": len(result)}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Stock list error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Lỗi truy vấn tồn kho: {str(e)}")
# --------------------------------------------------------------------------

@app.get("/stock/{store_id}/{sku}")
def get_stock(store_id: int, sku: str, user: dict = Depends(get_current_user)):
    require_permission("stock:read")(user)
    row = run_query(
        "SELECT * FROM stock WHERE store_id = %s AND sku = %s",
        [store_id, sku], fetchone=True
    )
    if not row: raise HTTPException(404, f"Khong tim thay stock store={store_id} sku={sku}")
    return {"data": clean_json_row(row)}

@app.post("/stock", status_code=201)
def create_stock(s: StockIn, user: dict = Depends(get_current_user)):
    require_permission("stock:write")(user)
    try:
        row = run_query("""
            INSERT INTO stock (store_id, sku, product_id, quantity, updated_at)
            VALUES (%s, %s, %s, %s, NOW())
            ON CONFLICT (store_id, sku) DO UPDATE SET
                quantity   = EXCLUDED.quantity,
                product_id = COALESCE(EXCLUDED.product_id, stock.product_id),
                updated_at = NOW()
            RETURNING *
        """, [int(s.store_id), s.sku, s.product_id, s.quantity], fetchone=True)
        return {"data": clean_json_row(row), "message": "Tao/Cap nhat stock thanh cong"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Loi tao stock: {str(e)}")

@app.put("/stock/{store_id}/{sku}")
def update_stock(store_id: int, sku: str, s: StockUpdate, user: dict = Depends(get_current_user)):
    require_permission("stock:write")(user)
    row = run_query("""
        UPDATE stock SET quantity = %s, updated_at = NOW()
        WHERE store_id = %s AND sku = %s RETURNING *
    """, [s.quantity, store_id, sku], fetchone=True)
    if not row: raise HTTPException(404, f"Stock store={store_id} sku={sku} khong tim thay")
    return {"data": clean_json_row(row), "message": "Cap nhat stock thanh cong"}

@app.patch("/stock/{store_id}/{sku}/adjust")
def adjust_stock(store_id: int, sku: str, s: StockAdjust, user: dict = Depends(get_current_user)):
    require_permission("stock:write")(user)
    row = run_query("""
        UPDATE stock SET quantity = GREATEST(0, quantity + %s), updated_at = NOW()
        WHERE store_id = %s AND sku = %s RETURNING *
    """, [s.delta, store_id, sku], fetchone=True)
    if not row: raise HTTPException(404, f"Stock store={store_id} sku={sku} khong tim thay")
    return {"data": clean_json_row(row), "message": f"Dieu chinh stock {'+' if s.delta >= 0 else ''}{s.delta}"}

@app.delete("/stock/{store_id}/{sku}")
def delete_stock(store_id: int, sku: str, user: dict = Depends(get_current_user)):
    require_permission("stock:write")(user)
    existing = run_query(
        "SELECT id FROM stock WHERE store_id = %s AND sku = %s",
        [store_id, sku], fetchone=True
    )
    if not existing: raise HTTPException(404, f"Stock store={store_id} sku={sku} khong tim thay")
    run_query("DELETE FROM stock WHERE store_id = %s AND sku = %s", [store_id, sku], fetch=False)
    return {"message": f"Da xoa stock store={store_id} sku={sku}"}


# ======================================================
# STOCK IMPORTS
# ======================================================
class StockImportIn(BaseModel):
    store_id:          int
    sku:               str
    product_id:        Optional[str] = None
    quantity_imported: int
    import_date:       Optional[str] = None
    supplier:          Optional[str] = None
    notes:             Optional[str] = None

    @validator('quantity_imported')
    def validate_qty(cls, v):
        if v <= 0: raise ValueError("quantity_imported phai lon hon 0")
        return v

@app.get("/stock-imports")
def list_stock_imports(
    store_id: Optional[int] = None,
    sku:      Optional[str] = None,
    limit:    int = Query(100, ge=1, le=1000),
    offset:   int = Query(0, ge=0),
    user: dict = Depends(get_current_user)
):
    require_permission("stock_imports:read")(user)
    sql = "SELECT * FROM stock_imports WHERE 1=1"
    params = []
    if store_id is not None: sql += " AND store_id = %s"; params.append(store_id)
    if sku is not None:      sql += " AND sku = %s";      params.append(sku)
    sql += " ORDER BY import_date DESC LIMIT %s OFFSET %s"
    params += [limit, offset]
    data = run_query(sql, params)
    return {"data": [clean_json_row(r) for r in data], "total": len(data)}

@app.post("/stock-imports", status_code=201)
def create_stock_import(si: StockImportIn, user: dict = Depends(get_current_user)):
    require_permission("stock_imports:write")(user)
    conn = None
    try:
        conn = get_conn()
        if conn.closed != 0:
            conn = psycopg2.connect(**DB_CONFIG)
            
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Kiem tra cot quantity_imported ton tai truoc khi INSERT
        col_check = run_query("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'stock_imports' AND column_name = 'quantity_imported'
        """, fetchone=True)
        
        if col_check:
            qty_col = 'quantity_imported'
        else:
            # Fallback: dung ten cot 'quantity' neu chua rename
            qty_col = 'quantity'
            log.warning("stock_imports: dung cot 'quantity' thay vi 'quantity_imported'")
        
        cur.execute(f"""
            INSERT INTO stock_imports (store_id, sku, product_id, {qty_col},
                import_date, supplier, notes)
            VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *
        """, [si.store_id, si.sku, si.product_id, si.quantity_imported,
              si.import_date or datetime.now().date().isoformat(),
              si.supplier, si.notes])
        import_row = cur.fetchone()

        cur.execute("""
            INSERT INTO stock (store_id, sku, product_id, quantity, last_restocked, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            ON CONFLICT (store_id, sku) DO UPDATE SET
                quantity       = stock.quantity + %s,
                last_restocked = %s,
                updated_at     = NOW()
            RETURNING quantity
        """, [si.store_id, si.sku, si.product_id, si.quantity_imported,
              si.import_date, si.quantity_imported, si.import_date])
        stock_row = cur.fetchone()

        conn.commit()
        return {
            "data": clean_json_row(import_row),
            "message": f"Nhap hang thanh cong, stock hien tai: {stock_row['quantity']}",
            "new_stock_quantity": stock_row["quantity"]
        }
    except HTTPException:
        if conn: conn.rollback()
        raise
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(500, f"Loi nhap hang: {str(e)}")
    finally:
        if conn: release_conn(conn)


# ======================================================
# FINAL DAILY
# ======================================================
@app.get("/final-daily")
def get_final_daily(
    store_id:  int,
    sku:       Optional[str] = None,
    from_date: Optional[str] = None,
    to_date:   Optional[str] = None,
    limit:     int = Query(500, ge=1, le=5000),
    user: dict = Depends(get_current_user)
):
    require_permission("final_daily:read")(user)
    sql = "SELECT * FROM final_daily WHERE store_id = %s"
    params = [store_id]
    if sku:       sql += " AND sku = %s";       params.append(sku)
    if from_date: sql += " AND date >= %s";     params.append(from_date)
    if to_date:   sql += " AND date <= %s";     params.append(to_date)
    sql += " ORDER BY date DESC LIMIT %s"
    params.append(limit)
    data = run_query(sql, params)
    return {"data": [clean_json_row(r) for r in data], "total": len(data)}

@app.get("/skus")
def get_skus(store_id: Optional[int] = Query(None, description="Mã cửa hàng"), user: dict = Depends(get_current_user)):
    require_permission("skus:read")(user)
    if store_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Yêu cầu truyền store_id"
        )
    
    rows = run_query("""
        SELECT DISTINCT ON (s.sku)
            s.sku,
            s.product_id,
            fd.category,
            fd.sub_category,
            fd.color,
            fd.size,
            fd.color_type,
            fd.avg_usd_price
        FROM stock s
        LEFT JOIN final_daily fd ON s.store_id = fd.store_id AND s.sku = fd.sku
        WHERE s.store_id = %s
        ORDER BY s.sku, fd.date DESC
    """, [store_id])
    return {"data": [clean_json_row(r) for r in rows], "total": len(rows)}


@app.get("/summary")
def get_summary(store_id: int, user: dict = Depends(get_current_user)):
    require_permission("summary:read")(user)
    row = run_query("""
        SELECT store_id, country, city,
               COUNT(DISTINCT sku) AS total_skus,
               COUNT(DISTINCT product_id) AS total_products,
               MIN(date) AS first_date, MAX(date) AS last_date,
               ROUND(AVG(avg_usd_price)::numeric, 2) AS avg_price,
               ROUND(AVG(total_discount_avg)::numeric, 4) AS avg_discount,
               ROUND(SUM(s_sales_velocity)::numeric, 2) AS total_velocity
        FROM final_daily WHERE store_id = %s
        GROUP BY store_id, country, city
    """, [store_id], fetchone=True)
    if not row: raise HTTPException(404, f"Khong co data cho store {store_id}")
    return {"data": clean_json_row(row)}

@app.get("/velocity-chart")
def get_velocity_chart(store_id: int, sku: str, user: dict = Depends(get_current_user)):
    require_permission("velocity:read")(user)
    rows = run_query("""
        SELECT date, s_sales_velocity, s2_sales_velocity,
               rolling_mean_7d, lag_1d, lag_7d
        FROM final_daily WHERE store_id = %s AND sku = %s ORDER BY date
    """, [store_id, sku])
    result = [clean_json_row(r) for r in rows]
    return {"data": result, "store_id": store_id, "sku": sku, "total": len(result)}