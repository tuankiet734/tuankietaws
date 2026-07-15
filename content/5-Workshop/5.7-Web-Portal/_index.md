---
title: "Web Portal & RBAC"
date: 2024-07-07
weight : 7
chapter: false
pre: " <b> 5.7. </b> "
---

### 5.7. Web Portal & Role-Based Access Control (Full-Stack Web App)

In Phase 4, we design and integrate the enterprise business intelligence portal (**Global Fashion Retail Portal**). The system ensures strict role-based user access controls, secure multi-factor authentication, and intelligent data visualization powered by AWS.

---

#### 1. Multi-mode Data Access Layer (DAL)

To operate flexibly across different environments (local development, testing, and cloud staging), the Node.js data access layer (`db.js`) supports **3 operational modes**:

*   **REST API Mode (API Mode):** Connects to the FastAPI Backend through AWS API Gateway when `API_BASE_URL` is configured. Requests are sent via Fetch with an HTTP Authorization Bearer Token.
*   **Real Database Mode (Real DB Mode):** Direct connection pool created via the PostgreSQL driver `pg` to the Amazon RDS instance (`training-db` or `fashion-rds`) based on `.env` credentials.
*   **Local Mock Mode (Mock JSON Mode):** An automatic fallback mechanism that reads and writes static JSON files under the `data/` directory when both API and direct database services are unreachable.

##### Multi-mode database routing logic:
```javascript
// db.js - Multi-mode data abstraction layer
const fs = require('fs');
const { Pool } = require('pg');

let dbMode = 'mock';
let pool = null;

if (process.env.API_BASE_URL) {
    dbMode = 'api';
    console.log("Database Mode: REST API Client active");
} else if (process.env.DB_HOST) {
    dbMode = 'postgres';
    pool = new Pool({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        database: process.env.DB_NAME,
        password: process.env.DB_PASSWORD,
        port: process.env.DB_PORT
    });
    console.log("Database Mode: Direct PostgreSQL Connection Pool active");
} else {
    console.log("Database Mode: Local Mock JSON active");
}
```

---

#### 2. Multi-Layer Secure Authentication (JWT & 2FA TOTP)

The platform protects corporate identities using encryption and multi-factor authentication:

1.  **JWT Tokens:** Login success grants a **JSON Web Token** valid for **8 hours** containing user identity claims (username, role, store_id) verified at backend endpoints.
2.  **TOTP Two-Factor Authentication (MFA):**
    *   Implements pure JavaScript HMAC-SHA1 hashing and Base32 decoding algorithms (without third-party dependencies) to validate 6-digit OTP codes changing every 30 seconds.
    *   Compatible with standard authenticator apps (Google Authenticator, Microsoft Authenticator) by generating shared secrets and QR codes (`otpauth://totp/`).
3.  **Audit Logs:** Records system events (`LOGIN`, `LOGIN_MFA`, `MFA_ENABLE`, `MFA_DISABLE`) mapped with user IP addresses and timestamps for security compliance.

---

#### 3. Role-Based Access Control (RBAC Matrix)

The system enforces a granular privilege matrix across **7 distinct business roles**:

| Role | Visibility Scope | Core Permissions / Actions |
| :--- | :--- | :--- |
| **IT Admin** | Global | `manage_users`, `manage_permissions`, `view_audit_logs`, `manage_inventory` |
| **Director** | Global | Super-user clearance (access to all Stores, Dashboard, Employees, and Transactions) |
| **Finance/Auditor** | Global | `view_all_stores`, `view_transactions`, `view_discounts`, `view_inventory` |
| **Inventory Manager** | Linked Store | `view_products`, `edit_products`, `view_inventory`, `manage_inventory` |
| **Marketing Manager** | Global | `view_all_stores`, `view_discounts`, `edit_discounts`, `view_inventory` |
| **Store Manager** | Linked Store | Complete staff management, inventory editing, transactions, and discount creation within store boundary |
| **Sales Staff** | Linked Store | View products, create cash register invoices (`create_transaction`), and add new customer entries |

> [!CAUTION]
> **Role Hierarchy Controls:** Administrative users are restricted to modifying accounts equal to or lower than their own rank, preventing system-level privilege escalation attacks.

---

#### 4. Interactive Maps & LightGBM Demand Forecast Dashboard

The main portal interface presents rich business intelligence widgets:

*   **Mapbox GL JS Integration:** Renders interactive 3D map markers representing retail stores worldwide.
*   **Skeleton Loader:** A spinning 3D earth visual loader displayed during initialization.
*   **Weekly Demand Forecast Panel:** Clicking any store marker:
    *   Fetches inference forecasts from the AWS-deployed **LightGBM** model via the `/predict` route.
    *   Plots an interactive **Plotly.js** chart comparing **Actual** quantities against **Forecasted** values over a weekly or monthly time horizon.
*   **Inventory Shortage Alerts:** Intersects physical warehouse stock levels with the coming week's forecasted demand, displaying a prominent red notification banner when a SKU requires restocking.

---

#### 5. Corporate Management Tabs

*   **Customers:** Searchable table including Plotly visualizations analyzing customer demographics (Gender Pie charts and Age Histograms).
*   **Discounts:** Tabulates current promotional rules and charts average markdown percentages (`total_discount_avg`).
*   **Employees:** Visualizes employee salary and sales performance metrics.
*   **Products:** Product catalog grid displaying clothing items alongside **images generated by Amazon Bedrock generative models** served from AWS S3.
*   **Stores:** Lists store details and SKU variety count.
*   **Transactions:** Invoices journal with search and currency filters that convert native currencies into standard USD totals.
*   **Inventory:** Manage warehouse inventory counts on a per-store basis.

---

#### 6. Modern Responsive UI/UX Design

*   **SPA Architecture (Single Page Application):** Navigates between dashboard views asynchronously via Fetch/AJAX calls without refreshing the page.
*   **Internationalization (i18n):** Real-time localization switching between **Vietnamese 🇻🇳**, **English 🇺🇸**, and **Chinese 🇨🇳** for headers, tables, alerts, and Plotly charts.
*   **Dark/Light Themes:** Harnesses custom HSL CSS variables and backdrop-blur glassmorphism layouts to deliver an eye-friendly theme configuration.
