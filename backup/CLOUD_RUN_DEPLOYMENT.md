# 🚀 Google Cloud Run Deployment - Rovnic Agentic AI

**Status:** Ready for production deployment  
**Platform:** Google Cloud Run  
**Region:** us-east1 (recommended)  
**Time to Deploy:** ~5-10 minutes  

---

## 📋 Prerequisites

Before deploying, ensure you have:

```bash
✅ Google Cloud Account (https://cloud.google.com)
✅ Google Cloud CLI installed (gcloud)
✅ Project created in Google Cloud Console
✅ Billing enabled on the project
✅ All environment variables ready
```

### Install Google Cloud CLI

**Windows/macOS:**
```bash
# Download and install from:
https://cloud.google.com/sdk/docs/install
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

### Verify Installation
```bash
gcloud --version
gcloud auth login
gcloud projects list
```

---

## 🔧 Setup Steps

### Step 1: Set Project ID

```bash
# Set your Google Cloud project
gcloud config set project YOUR_PROJECT_ID

# Verify
gcloud config list
```

### Step 2: Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Step 3: Configure Docker Registry (Optional)

For automatic build and push to Google Container Registry:

```bash
gcloud auth configure-docker gcr.io
```

---

## 🚀 Deploy to Cloud Run

### Method 1: Direct Deployment (Easiest)

```bash
cd C:\Users\afeson\rovnic_agentic_ai\rovnic-agentic-ai

gcloud run deploy rovnic-agent-api \
  --source . \
  --region us-east1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 100 \
  --min-instances 0 \
  --set-env-vars \
    OPENAI_API_KEY=sk-your-openai-key,\
    ODDS_API_KEY=your-odds-api-key,\
    FIREBASE_KEY_PATH=/secrets/firebase-key.json,\
    AWS_ACCESS_KEY_ID=your-aws-key,\
    AWS_SECRET_ACCESS_KEY=your-aws-secret,\
    AWS_S3_BUCKET=rovnic-voice-summaries,\
    ENVIRONMENT=production,\
    LOG_LEVEL=INFO
```

### Method 2: Build and Push Manually

**Step 1: Build Docker image**
```bash
docker build -t rovnic-agent-api .
```

**Step 2: Tag for Google Container Registry**
```bash
docker tag rovnic-agent-api gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:latest
```

**Step 3: Push to registry**
```bash
docker push gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:latest
```

**Step 4: Deploy from registry**
```bash
gcloud run deploy rovnic-agent-api \
  --image gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:latest \
  --region us-east1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 100 \
  --set-env-vars \
    OPENAI_API_KEY=sk-your-key,\
    ODDS_API_KEY=your-key,\
    AWS_ACCESS_KEY_ID=your-key,\
    AWS_SECRET_ACCESS_KEY=your-secret,\
    AWS_S3_BUCKET=rovnic-voice-summaries
```

---

## 📊 Resource Configuration

### Recommended Settings

```bash
# Memory and CPU
--memory 1Gi           # 1 GB RAM (suitable for API)
--cpu 2                # 2 CPUs

# Scaling
--max-instances 100    # Max concurrent instances
--min-instances 0      # Scale to zero when idle

# Timeout
--timeout 300          # 5 minutes (for long prediction cycles)

# Concurrency
--concurrency 80       # Requests per instance
```

### For Higher Load

```bash
gcloud run deploy rovnic-agent-api \
  --image gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:latest \
  --region us-east1 \
  --memory 2Gi \
  --cpu 4 \
  --max-instances 200 \
  --min-instances 1 \
  --concurrency 100
```

---

## 🔐 Manage Secrets (Firebase Key)

For sensitive data like Firebase credentials:

### Create Secret

```bash
# Create a secret
echo "$(cat firebase-key.json)" | gcloud secrets create firebase-key --data-file=-

# Or interactively
gcloud secrets create firebase-key
```

### Grant Access

```bash
# Get Cloud Run service account
PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format='value(projectNumber)')
SERVICE_ACCOUNT="$PROJECT_NUMBER-compute@developer.gserviceaccount.com"

# Grant secret accessor role
gcloud secrets add-iam-policy-binding firebase-key \
  --member=serviceAccount:$SERVICE_ACCOUNT \
  --role=roles/secretmanager.secretAccessor
```

### Use in Deployment

```bash
gcloud run deploy rovnic-agent-api \
  --image gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:latest \
  --region us-east1 \
  --update-secrets FIREBASE_KEY=/secrets/firebase-key:latest \
  --set-env-vars FIREBASE_KEY_PATH=/run/secrets/firebase-key
```

---

## ✅ Verify Deployment

### Get Service URL

```bash
gcloud run services describe rovnic-agent-api --region us-east1 --format='value(status.url)'
```

### Test Health Endpoint

```bash
SERVICE_URL=$(gcloud run services describe rovnic-agent-api --region us-east1 --format='value(status.url)')

curl $SERVICE_URL/health

# Expected response:
# {"status":"healthy","timestamp":"2025-10-28T15:30:00Z"}
```

### Test Prediction Endpoint

```bash
curl $SERVICE_URL/api/nba

# Expected response:
# {"sport":"NBA","game":"Team A vs Team B","prediction":"Win",...}
```

### View Logs

```bash
gcloud run logs read rovnic-agent-api --region us-east1 --limit 100

# Follow logs in real-time
gcloud run logs read rovnic-agent-api --region us-east1 --follow
```

---

## 📈 Monitor Deployment

### View Metrics

```bash
gcloud run describe rovnic-agent-api --region us-east1

# See:
# - URL
# - Revisions
# - Memory
# - CPU
# - Instances
```

### Set Up Cloud Monitoring

```bash
# View in Cloud Console
# https://console.cloud.google.com/run/detail/us-east1/rovnic-agent-api/metrics
```

---

## 🔄 Update Deployment

### Deploy New Version

```bash
# After code changes and docker rebuild
docker build -t gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:v2 .
docker push gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:v2

gcloud run deploy rovnic-agent-api \
  --image gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:v2 \
  --region us-east1
```

### Rollback to Previous Version

```bash
gcloud run rollbacks create rovnic-agent-api --region us-east1
```

---

## 💰 Cost Estimation

**Estimated Monthly Cost (us-east1):**

- **Compute:** ~$10-30 (based on 0-1 instances, 1Gi RAM)
- **Networking:** ~$5-15 (egress data)
- **Storage:** ~$5-10 (container registry)
- **Total:** ~$20-55/month

**Cost Optimization:**
- Use `--min-instances 0` to scale to zero when idle
- Monitor usage in Cloud Console
- Set up budget alerts

---

## 🐛 Troubleshooting

### Issue: "Permission denied" on deploy

**Solution:**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Issue: "Container failed to start"

**Check logs:**
```bash
gcloud run logs read rovnic-agent-api --region us-east1 --limit 50
```

**Common causes:**
- Missing environment variables
- API key invalid
- Port not 8000

### Issue: "Timeout errors"

**Solution:**
```bash
gcloud run deploy rovnic-agent-api \
  --timeout 600 \
  --region us-east1
```

### Issue: "Out of memory"

**Solution:**
```bash
gcloud run deploy rovnic-agent-api \
  --memory 2Gi \
  --region us-east1
```

---

## 🎯 Complete Deployment Command

**One-liner for complete deployment:**

```bash
cd C:\Users\afeson\rovnic_agentic_ai\rovnic-agentic-ai && \
docker build -t gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:latest . && \
docker push gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:latest && \
gcloud run deploy rovnic-agent-api \
  --image gcr.io/YOUR_PROJECT_ID/rovnic-agent-api:latest \
  --region us-east1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 100 \
  --set-env-vars OPENAI_API_KEY=sk-your-key,ODDS_API_KEY=your-key,AWS_ACCESS_KEY_ID=your-key,AWS_SECRET_ACCESS_KEY=your-secret,AWS_S3_BUCKET=rovnic-voice-summaries
```

---

## 📚 Additional Resources

- **Cloud Run Documentation:** https://cloud.google.com/run/docs
- **Cloud Run Pricing:** https://cloud.google.com/run/pricing
- **Cloud Run Best Practices:** https://cloud.google.com/run/docs/quickstarts/build-and-deploy
- **Secrets Manager:** https://cloud.google.com/secret-manager/docs

---

## ✅ Final Checklist

- [ ] Google Cloud account created
- [ ] Project ID set
- [ ] APIs enabled (Run, Build, Registry)
- [ ] Environment variables prepared
- [ ] Docker image built
- [ ] Deployment command ready
- [ ] Test endpoints working
- [ ] Logs monitoring configured
- [ ] Cost alerts set up

---

## 🎉 Deployment Ready!

Your Rovnic Agentic AI will be live on Google Cloud Run within minutes!

**Command to deploy:**
```bash
gcloud run deploy rovnic-agent-api --source . --region us-east1
```

**After deployment:**
- Service URL provided
- Auto-scaling enabled
- HTTPS enabled
- Global CDN available

🚀 **Ready to launch!**
