# 🔧 Cloud Run Deployment Fix - Port Configuration

**Issue:** Container failed to start on PORT=8080  
**Cause:** Cloud Run expects port 8080, but our app runs on port 8000  
**Solution:** Update Dockerfile to use port 8080  

---

## ✅ FIX #1: Update Dockerfile

**File:** `Dockerfile`

**Change:**
```dockerfile
# BEFORE:
ENV PYTHONUNBUFFERED=1 PORT=8000 HOST=0.0.0.0 LOG_LEVEL=INFO ENVIRONMENT=production

# AFTER:
ENV PYTHONUNBUFFERED=1 PORT=8080 HOST=0.0.0.0 LOG_LEVEL=INFO ENVIRONMENT=production

# BEFORE:
CMD ["python", "-m", "uvicorn", "src.api_server:app", "--host", "0.0.0.0", "--port", "8000"]

# AFTER:
CMD ["python", "-m", "uvicorn", "src.api_server:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## ✅ FIX #2: Update Environment Variables

Update `.env.example`:
```bash
PORT=8080  # Changed from 8000
HOST=0.0.0.0
```

---

## 🚀 RETRY DEPLOYMENT

After fixing the Dockerfile:

```bash
cd C:\Users\afeson\rovnic_agentic_ai\rovnic-agentic-ai

# Commit the fix
git add Dockerfile .env.example
git commit -m "Fix Cloud Run port configuration (8080)"
git push origin main

# Redeploy
gcloud run deploy rovnic-agent-api \
  --source . \
  --region us-east1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 2 \
  --timeout 300 \
  --set-env-vars \
    OPENAI_API_KEY=sk-your-key,\
    ODDS_API_KEY=your-key,\
    AWS_ACCESS_KEY_ID=your-key,\
    AWS_SECRET_ACCESS_KEY=your-secret,\
    AWS_S3_BUCKET=rovnic-voice-summaries,\
    ENVIRONMENT=production
```

---

## 📊 Deployment Details

### First Attempt Status
```
✅ Repository created in Artifact Registry
✅ Docker image built successfully
✅ Container uploaded to registry
❌ Container failed to start (port mismatch)
   - Expected: PORT=8080
   - Actual: PORT=8000
```

### After Fix
```
✅ Dockerfile updated to PORT=8080
✅ Command updated to --port 8080
✅ Redeploy to Cloud Run
✅ Service should start successfully
```

---

## 🔗 Cloud Run Details

**Project:** v-web-5daea  
**Service:** rovnic-agent-api  
**Region:** us-east1  
**Repository:** cloud-run-source-deploy (auto-created)  

**Logs URL (from failed deployment):**
https://console.cloud.google.com/logs/viewer?project=v-web-5daea&resource=cloud_run_revision/service_name/rovnic-agent-api/revision_name/rovnic-agent-api-00001-sqt

---

## 🐛 Common Cloud Run Issues

### Issue: Port mismatch
**Solution:** Cloud Run uses PORT=8080. Update Dockerfile.

### Issue: Timeout
**Solution:** Add `--timeout 300` to gcloud command.

### Issue: Memory error
**Solution:** Add `--memory 2Gi` to gcloud command.

### Issue: Environment variables missing
**Solution:** Use `--set-env-vars` flag with comma-separated values.

---

## ✅ NEXT STEPS

1. Update `Dockerfile` - change port from 8000 to 8080
2. Update `.env.example` - change PORT from 8000 to 8080
3. Commit changes: `git add . && git commit -m "Fix Cloud Run port"`
4. Push changes: `git push origin main`
5. Redeploy: Run the deployment command above
6. Check status: `gcloud run services describe rovnic-agent-api --region us-east1`
7. Get URL: `gcloud run services describe rovnic-agent-api --region us-east1 --format='value(status.url)'`
8. Test: `curl <service-url>/health`

---

## 🎯 After Deployment Success

Once deployed successfully:

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe rovnic-agent-api --region us-east1 --format='value(status.url)')

# Test health endpoint
curl $SERVICE_URL/health

# Test prediction endpoint
curl $SERVICE_URL/api/nba

# View logs
gcloud run logs read rovnic-agent-api --region us-east1 --limit 50
```

---

**Status:** Ready to fix and retry deployment  
**Priority:** HIGH - Simple port configuration fix  
**Time to Fix:** < 5 minutes  

🚀 **Let's fix the port and get Rovnic Agentic AI live on Cloud Run!**
