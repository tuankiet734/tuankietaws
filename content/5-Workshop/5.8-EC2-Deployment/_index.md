---
title: "Web App EC2 Deployment"
date: 2024-07-07
weight : 8
chapter: false
pre: " <b> 5.8. </b> "
---

### 5.8. Web Application Deployment on AWS EC2

The objective of Phase 5 is to deploy the Web Application code to the Cloud Production Server (**Amazon EC2**) and connect all the AWS services deployed in previous phases: Amazon RDS, AWS Lambda / API Gateway, Amazon S3, and Amazon Cognito.

---

#### STEP 1: Launching the EC2 Instance on the AWS Console

##### 1.1 Launch Instance:
1. Open the **AWS Management Console**, search for **EC2**.
2. From the **EC2 Dashboard**, click the orange **Launch instance** button.

##### 1.2 Configure Name and OS (AMI):
*   **Name:** Set the server name to `fashion-web-server`.
*   **Application and OS Images (AMI):** Select **Ubuntu**, then choose the **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type** (64-bit x86) image.

##### 1.3 Configure Instance Type & Key Pair:
*   **Instance type:** Locate and select the `t3.large` instance type (2 vCPUs, 8 GiB RAM) to ensure adequate computing resources for handling the Web Portal rendering and interactive Plotly graphs.
*   **Key pair:** Select an existing key pair or click **Create new key pair** to generate a `.pem` file (named `fashion-key.pem`) for SSH authentication.

##### 1.4 Security Group Configuration (Inbound Rules):
Under **Network settings**, choose **Create security group**, name it `web-app-sg`, and add the following Inbound rules:

| Type | Protocol | Port Range | Source | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **SSH** | TCP | `22` | `My IP` | Secure remote shell administration |
| **HTTP** | TCP | `80` | `0.0.0.0/0` | Handles public HTTP web traffic |
| **HTTPS** | TCP | `443` | `0.0.0.0/0` | Handles encrypted HTTPS SSL traffic |
| **Custom TCP** | TCP | `3000` | `10.0.0.0/16` | Internal VPC access for the Node.js application |
| **Custom TCP** | TCP | `8000` | `10.0.0.0/16` | Internal VPC access for the FastAPI backend service |

*   **Configure storage:** Allocate a minimum of **20 GiB gp3** SSD storage to handle library installations and logging.
*   Click **Launch instance** and wait for the instance state to transition to `Running`.

---

#### STEP 2: Connecting via SSH and Setting Up the Environment

##### 2.1 SSH Connection:
Open your PowerShell (Windows) or Terminal (macOS/Linux) and navigate to the directory containing your `.pem` key file:
```bash
# Modify file permissions for the key (macOS/Linux only)
chmod 400 fashion-key.pem

# Establish SSH connection (replace with your EC2 Public IP address)
ssh -i "fashion-key.pem" ubuntu@<PUBLIC_IP_EC2>
```

##### 2.2 Installing Base Utilities:
Once connected to the EC2 Ubuntu terminal, execute the following commands to install Node.js 20.x, Nginx, PM2, PostgreSQL client, and the AWS CLI:
```bash
# 1. Update and upgrade system packages
sudo apt update && sudo apt upgrade -y

# 2. Install the Nginx Web Server
sudo apt install nginx -y

# 3. Add Node.js 20.x repository and install Node
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# 4. Verify package versions
node -v   # Should output v20.x.x
npm -v    # Should output v10.x.x

# 5. Install PM2 globally to manage background Node.js processes
sudo npm install -g pm2

# 6. Install the AWS CLI and PostgreSQL client tools
sudo apt install awscli postgresql-client -y
```

---

#### STEP 3: Deploying Code and Configuring the Environment (.env)

##### 3.1 Clone the Application:
```bash
# Create application directory
mkdir -p /home/ubuntu/app
cd /home/ubuntu/app

# Clone your GitHub repository (replace with your repository URL)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .
```

##### 3.2 Initialize the Secure Environment File (`.env`):
Create a `.env` configuration file using Nano:
```bash
nano .env
```
Paste your database, API, and credential settings:
```env
# ======= DATABASE – Amazon RDS =======
DB_HOST=training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=fashiondb
DB_USER=dbadmin
DB_PASSWORD=Tung2004

# ======= AWS SERVICES =======
AWS_REGION=ap-southeast-1
S3_BUCKET_NAME=fashion-retail-model-storage
API_GATEWAY_URL=https://5e0wzdirtc.execute-api.ap-southeast-1.amazonaws.com/dev

# ======= AUTHENTICATION =======
JWT_SECRET=fashion_secret_key_jwt_token_retail_portal_2026
COGNITO_USER_POOL_ID=ap-southeast-1_XXXXXXXX
COGNITO_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx

# ======= APP CONFIG =======
NODE_ENV=production
PORT=3000
```
*Press `Ctrl + O` to write out, and `Ctrl + X` to exit.*

> [!CAUTION]
> Never commit your `.env` file to git repositories to protect database and cloud authorization credentials from leak hazards.

##### 3.3 Install Dependencies:
```bash
npm install --production
```

---

#### STEP 4: Configuring PM2 for Continuous Application Running

PM2 keeps your Node.js application running in the background and restarts the process if it encounters a fatal crash:

```bash
# Launch the Express.js application named "fashion-web"
pm2 start app.js --name "fashion-web" --env production

# Verify the process is active (the status column should display green 'online')
pm2 list

# Configure PM2 to automatically launch during system boot
pm2 startup
```
*Note: The `pm2 startup` command will display a `sudo env PATH=...` block. Copy and execute that specific command to finalize the systemd integration.*

```bash
# Save current PM2 processes list
pm2 save
```

---

#### STEP 5: Setting Up Nginx as a Reverse Proxy

Nginx acts as the front gateway receiving public HTTP traffic on port 80 and routing requests safely to the local Node.js application on port 3000, while serving static file assets efficiently.

##### 5.1 Create Nginx Site Configuration:
```bash
sudo nano /etc/nginx/sites-available/fashion-app
```
Add the server block structure (replace with your registered domain name or public IP):
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    client_max_body_size 20M;

    location / {
        proxy_pass         http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection 'upgrade';
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 90;
    }

    location /static {
        alias   /home/ubuntu/app/public;
        expires 30d;
    }
}
```

##### 5.2 Activate Configurations and Restart Nginx:
```bash
# Link the configuration to the enabled folder
sudo ln -s /etc/nginx/sites-available/fashion-app /etc/nginx/sites-enabled/

# Remove Nginx's default config to prevent port 80 conflicts
sudo rm /etc/nginx/sites-enabled/default

# Verify Nginx configuration syntax (must report: syntax is ok, test is successful)
sudo nginx -t

# Restart the Nginx daemon
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

#### STEP 6: Installing SSL/HTTPS Certificates with Certbot

To secure network logins and API transactions between clients and the server, provision a free SSL certificate from **Let's Encrypt**:

```bash
# Install certbot and its nginx helper module
sudo apt install certbot python3-certbot-nginx -y

# Request and configure SSL certificates (replace with your active A-Record domain)
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Verify automated certificate renewal (Let's Encrypt certificates expire in 90 days)
sudo certbot renew --dry-run
```

---

#### STEP 7: Testing Integrations with AWS Cloud Services

Once deployed, run the following diagnostic commands from the EC2 terminal to verify direct network connectivity to your AWS resources:

##### 7.1 Verify RDS Connection:
```bash
psql -h training-db.c7846wiue0od.ap-southeast-1.rds.amazonaws.com \
     -U dbadmin -d fashiondb \
     -c "SELECT COUNT(*) FROM stores;"
```
*Expected output: Returns active retail stores count.*

##### 7.2 Verify API Gateway & Lambda Forecast API:
```bash
curl -X POST https://5e0wzdirtc.execute-api.ap-southeast-1.amazonaws.com/dev/predict \
  -H "Content-Type: application/json" \
  -H "x-api-key: YEUnLELr4c4tqQdnToSw43sYJRqIKBrd5WDYxZH9" \
  -d '{"store_id":"20","sku":"FESH6946-S-","date":"2025-03-18"}'
```
*Expected output: Responds with a 200 HTTP code and the predicted demand payload.*

##### 7.3 Verify Amazon S3 Access:
```bash
aws s3 ls s3://fashion-retail-model-storage/models/ --region ap-southeast-1
```
*Expected output: Lists the three serialized model pickle files.*

---

#### STEP 8: End-to-End System Testing

Open a web browser and navigate to `https://your-domain.com` (or your EC2 instance's Public IP). Complete the following checklist matching user roles:

| Step | User Login Role | Test Actions | Expected Results |
| :--- | :--- | :--- | :--- |
| **8.1** | **Sales Staff** | Log in with staff credentials | Access granted. Navigation sidebar is restricted and only displays the *Transactions* and *Products* tabs. |
| **8.2** | **Store Manager** | Log in with manager credentials | Access granted. Able to edit and update *Discounts* and *Employees* within their assigned store boundary. |
| **8.3** | **Director** | Log in with director credentials | Access granted. *Dashboard* tab displays the **Mapbox** component. Clicking a store marker displays interactive **Plotly.js** Actual vs. Forecasted graphs fetched from the AWS Lambda API. |

---

#### APPENDIX: Troubleshooting Common Deployment Issues

1.  **`502 Bad Gateway` Error:**
    *   *Cause:* The Node.js application on port 3000 is stopped or crashed.
    *   *Solution:* Run `pm2 logs fashion-web` to identify errors and restart it with `pm2 restart fashion-web`.
2.  **RDS Database Connection Timeout:**
    *   *Cause:* The RDS Security Group is blocking inbound traffic on port 5432 from the EC2 instance IP.
    *   *Solution:* Open the RDS Dashboard -> Connectivity & security -> Click on your VPC Security Group and add an Inbound rule permitting port 5432 from the EC2's security group.
3.  **Product Images Fail to Render:**
    *   *Cause:* The EC2 instance lacks permissions to read from the S3 bucket.
    *   *Solution:* Attach an IAM Instance Profile containing `AmazonS3ReadOnlyAccess` permissions to your EC2 instance.
4.  **`403 Forbidden` on Forecast API Request:**
    *   *Cause:* Invalid or missing `x-api-key` in header metadata.
    *   *Solution:* Double check the `API_GATEWAY_URL` and `x-api-key` configurations inside the backend `.env` file.
