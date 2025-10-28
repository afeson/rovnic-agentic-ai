# 🚀 Deployment Guide - Rovnic Agentic AI

Complete guide for deploying Rovnic Agentic AI to various environments.

---

## 📋 Prerequisites

✅ Python 3.11+  
✅ Git  
✅ Docker (for containerized deployment)  
✅ Google Cloud CLI (for Cloud Run)  
✅ AWS CLI (for AWS deployment)  

---

## 🏠 Local Development

### 1. Clone Repository
```bash
git clone <repo-url>
cd rovnic-agentic-ai
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env

# Edit .env with your keys:
# ODDS_API_KEY=...
# OPENAI_API_KEY=...
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...
# FIREBASE_KEY_PATH=./firebase-key.json
```

### 5. Add Firebase Key
```bash
cp /path/to/firebase-key.json ./firebase-key.json
```

### 6. Run Locally

**Option A: Start API Server**
```bash
uvicorn src.api_server:app --reload --port 8000
```

Access: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`

**Option B: Start Scheduler**
```bash
python src/main.py
```

---

## 🐳 Docker Deployment

### 1. Build Docker Image
```bash
docker build -t rovnic-agent:latest .
```

### 2. Run Container Locally
```bash
docker run -p 8000:8000 \
  -e ODDS_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_key \
  -v $(pwd)/firebase-key.json:/app/firebase-key.json \
  rovnic-agent:latest
```

### 3. Test Container
```bash
curl http://localhost:8000/health
```

---

## ☁️ Google Cloud Run (Recommended)

### 1. Prerequisites
```bash
gcloud init
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Create Cloud Storage Bucket
```bash
gsutil mb gs://rovnic-agent-bucket
```

### 3. Deploy to Cloud Run
```bash
gcloud run deploy rovnic-agent-api \
  --source . \
  --region us-east1 \
  --allow-unauthenticated \
  --platform managed \
  --memory 1Gi \
  --timeout 300 \
  --set-env-vars \
    ODDS_API_KEY=your_key,\
    OPENAI_API_KEY=your_key,\
    AWS_ACCESS_KEY_ID=your_key,\
    AWS_SECRET_ACCESS_KEY=your_key,\
    FIREBASE_KEY_PATH=/secrets/firebase-key.json,\
    ENVIRONMENT=production
```

### 4. Add Firebase Secret
```bash
# Create secret
echo "$(cat firebase-key.json)" | gcloud secrets create firebase-key --data-file=-

# Mount in Cloud Run (update deployment)
gcloud run deploy rovnic-agent-api \
  --update-secrets firebase-key=/secrets/firebase-key:latest \
  ...
```

### 5. Get Service URL
```bash
gcloud run services describe rovnic-agent-api --region us-east1
```

---

## 🌐 AWS Lambda Deployment

### 1. Prepare Package
```bash
# Install dependencies
pip install -r requirements.txt -t .

# Create deployment package
zip -r rovnic-agent.zip .

# Upload to S3
aws s3 cp rovnic-agent.zip s3://rovnic-agent-lambda/
```

### 2. Create Lambda Function
```bash
aws lambda create-function \
  --function-name rovnic-agent-api \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-role \
  --handler src.api_server.app \
  --zip-file fileb://rovnic-agent.zip \
  --memory-size 1024 \
  --timeout 300 \
  --environment "Variables={
    ODDS_API_KEY=your_key,
    OPENAI_API_KEY=your_key,
    FIREBASE_KEY_PATH=/tmp/firebase-key.json
  }"
```

### 3. Add API Gateway
```bash
aws apigatewayv2 create-api \
  --name rovnic-agent-api \
  --protocol-type HTTP \
  --target arn:aws:lambda:us-east-1:YOUR_ID:function:rovnic-agent-api
```

### 4. Deploy
```bash
aws lambda update-function-code \
  --function-name rovnic-agent-api \
  --s3-bucket rovnic-agent-lambda \
  --s3-key rovnic-agent.zip
```

---

## 🖥️ AWS EC2 Deployment

### 1. Launch EC2 Instance
```bash
# Ubuntu 22.04 LTS recommended
# t3.medium or larger
# Security group: Allow inbound 8000 (HTTP), 443 (HTTPS), 22 (SSH)
```

### 2. SSH into Instance
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

### 3. Setup Environment
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3-pip -y

# Clone repository
git clone <repo-url>
cd rovnic-agentic-ai

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Create .env
nano .env

# Add all required variables
```

### 5. Create systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/rovnic-agent.service
```

**Content:**
```ini
[Unit]
Description=Rovnic Agentic AI API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/rovnic-agentic-ai
ExecStart=/usr/bin/python3 -m uvicorn src.api_server:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 6. Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable rovnic-agent
sudo systemctl start rovnic-agent
sudo systemctl status rovnic-agent
```

### 7. Setup Nginx Reverse Proxy (Optional)
```bash
sudo apt install nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/rovnic-agent
```

**Content:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 8. Enable Nginx
```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

## 🔐 SSL/TLS Setup (AWS Certificate Manager)

### 1. Request Certificate
```bash
aws acm request-certificate \
  --domain-name your-domain.com \
  --subject-alternative-names "*.your-domain.com" \
  --validation-method DNS
```

### 2. Validate Certificate
Follow AWS Certificate Manager validation steps

### 3. Attach to Load Balancer
```bash
aws elbv2 create-load-balancer \
  --name rovnic-agent-lb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx
```

---

## 📊 Monitoring & Logging

### Cloud Run Logs
```bash
gcloud run logs read rovnic-agent-api --region us-east1 --limit 100
```

### EC2 Logs
```bash
sudo journalctl -u rovnic-agent -f
tail -f logs/app.log
```

### Cloud Monitoring
```bash
gcloud monitoring dashboards create --config-from-file=dashboard.json
```

---

## 🚨 Health Checks

### Local
```bash
curl http://localhost:8000/health
```

### Cloud Run
```bash
curl https://rovnic-agent-api.run.app/health
```

### Metrics
```bash
curl http://your-url/metrics
```

---

## 🔧 Environment Configuration

Key environment variables for production:

```bash
# API Keys
ODDS_API_KEY=your_odds_key
OPENAI_API_KEY=your_openai_key

# Firebase
FIREBASE_KEY_PATH=/secrets/firebase-key.json

# AWS
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=rovnic-voice-summaries

# Model Config
PREDICTION_MODEL=gpt-4.1-mini
EXPLANATION_MODEL=gpt-4.1-mini

# Performance
ACCURACY_THRESHOLD=0.80
RETRAINING_MIN_PREDICTIONS=10
ROLLING_WINDOW_DAYS=7
REFRESH_INTERVAL_HOURS=4

# Server
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=production
LOG_LEVEL=INFO
```

---

## 📈 Scaling

### Horizontal Scaling (Cloud Run)
```bash
gcloud run deploy rovnic-agent-api \
  --max-instances 100 \
  --concurrency 80
```

### Load Balancing (AWS)
```bash
aws elbv2 create-target-group \
  --name rovnic-agent-targets \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxx
```

---

## 🔍 Troubleshooting

### Issue: "Firestore connection failed"
**Solution:** Check firebase-key.json path and credentials

### Issue: "Odds API timeout"
**Solution:** Check ODDS_API_KEY and network connectivity

### Issue: "S3 upload failed"
**Solution:** Verify AWS credentials and bucket permissions

### Issue: "Model not found"
**Solution:** Ensure models/model.pkl exists in deployment

---

## ✅ Deployment Checklist

- [ ] All environment variables configured
- [ ] Firebase key deployed and accessible
- [ ] AWS S3 bucket created and accessible
- [ ] Models (model.pkl, scaler.pkl) deployed
- [ ] Health check passes (`/health` endpoint)
- [ ] Predictions endpoint works (`/api/nba`)
- [ ] Firestore data appears in console
- [ ] S3 audio files upload successfully
- [ ] Logs are being written
- [ ] SSL certificate installed (production)
- [ ] Rate limiting configured
- [ ] Monitoring/alerts setup
- [ ] Backup strategy in place

---

## 🎉 Production Ready!

Your Rovnic Agentic AI is now deployed and ready to handle real predictions for all 8 sports.

**Next Steps:**
1. Configure Rovnic.com frontend to request from `/api/{sport}`
2. Monitor accuracy metrics dashboard
3. Set up automated retraining jobs
4. Configure CI/CD pipeline for updates
