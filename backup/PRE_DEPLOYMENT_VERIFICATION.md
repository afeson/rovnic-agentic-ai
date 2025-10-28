# 🔍 PRE-DEPLOYMENT VERIFICATION CHECKLIST

**Date:** October 28, 2025  
**System:** Rovnic Agentic AI  
**Status:** READY FOR VERIFICATION  

---

## ✅ VERIFICATION STEPS

### 1️⃣ Environment Configuration Verification

**Required Variables in `.env`:**

```ini
# CRITICAL - Must NOT be empty
OPENAI_API_KEY=sk-your-key-here
ODDS_API_KEY=your-odds-api-key
FIREBASE_KEY_PATH=./firebase-key.json
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=rovnic-voice-summaries

# OPTIONAL but recommended
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=production
LOG_LEVEL=INFO
ACCURACY_THRESHOLD=0.80
```

**Verification Command:**
```bash
# Check if .env exists and is configured
cat .env | grep -v "^#" | grep "="
```

**Expected Output:**
- All 6 critical keys populated (not empty)
- No error messages
- Valid format: KEY=VALUE

---

### 2️⃣ Local API Server Launch

**Command:**
```bash
uvicorn src.api_server:app --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Verification:**
- Server starts without errors
- Port 8000 accessible
- FastAPI docs load at `http://localhost:8000/docs`
- Health check returns 200: `curl http://localhost:8000/health`

**Health Check Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-28T15:30:00Z"
}
```

---

### 3️⃣ Prediction Pipeline Test

**Command:**
```bash
python src/main.py
```

**Expected Workflow:**
1. [FETCH] Fetches live odds for all 8 sports
2. [PREDICT] ML model runs predictions
3. [ANALYZE] GPT-4.1-mini generates analysis
4. [VOICE] OpenAI TTS creates MP3
5. [SAVE] Stores to Firestore
6. [SUCCESS] Cycle complete

**Expected Output:**
```
[META] Rovnic Meta-Learning Supervisor started
[CYCLE] Starting 4-hour prediction cycle
[FETCH] Fetching live odds for NBA...
[PREDICT] Running ML for NBA...
[ANALYZE] AI analysis for NBA...
[VOICE] Generating voice for NBA...
[SAVE] Saving to Firestore for NBA...
[SUCCESS] Cycle complete: 8/8 successful
```

**Success Criteria:**
- ✅ No import errors
- ✅ All 8 sports processed
- ✅ Predictions generated with confidence scores
- ✅ AI analysis completed
- ✅ Voice file generated
- ✅ Firestore save successful

---

### 4️⃣ Firestore & S3 Integration Verification

**Firestore Path Check:**
```
/predictions/{sport}/{date}/{game_id}
Example: /predictions/NBA/2025-10-28/LAL_vs_BOS
```

**Expected Firestore Document:**
```json
{
  "sport": "NBA",
  "game": "Team A vs Team B",
  "prediction": "Win",
  "confidence": 0.87,
  "analysis": "AI-generated analysis...",
  "audio_url": "https://rovnic-voice-summaries.s3.amazonaws.com/nba/abc123.mp3",
  "timestamp": "2025-10-28T15:30:00Z"
}
```

**AWS S3 Check:**
- Bucket: `rovnic-voice-summaries`
- MP3 files uploaded to: `{sport}/{uuid}.mp3`
- Files are publicly accessible

**Verification Commands:**
```bash
# Check Firestore (from Firebase Console)
https://console.firebase.google.com

# Check S3 (from AWS Console)
https://s3.console.aws.amazon.com/s3/
```

---

### 5️⃣ Auto-Retraining Agent Test

**Command:**
```bash
python src/agents/retrain_agent.py
```

**Expected Output:**
```
[RETRAIN] Triggering retraining for NBA...
[1/4] Fetching recent predictions...
[2/4] Preparing training data...
[3/4] Retraining model...
[4/4] Validating model...
[RETRAIN] Retraining completed for NBA with accuracy 85.0%
```

**Success Criteria:**
- ✅ All 4 steps complete
- ✅ New accuracy score displayed
- ✅ Model saved to `models/model.pkl`
- ✅ No errors or exceptions

---

### 6️⃣ Dependency & Import Verification

**Command:**
```bash
python -c "import fastapi, uvicorn, openai, firebase_admin, boto3, schedule, requests, numpy, joblib; print('All imports successful!')"
```

**Expected Output:**
```
All imports successful!
```

**Missing Module Check:**
```bash
python -m pip check
```

**Expected Output:**
```
No broken requirements found.
```

---

## 📋 QUICK VERIFICATION SCRIPT

Create `verify.sh` and run:

```bash
#!/bin/bash

echo "🔍 ROVNIC AGENTIC AI - PRE-DEPLOYMENT VERIFICATION"
echo "=============================================="
echo ""

# 1. Check .env
echo "1️⃣ Checking .env configuration..."
if [ -f .env ]; then
  MISSING=$(grep -E "^(OPENAI_API_KEY|ODDS_API_KEY|FIREBASE_KEY_PATH|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_S3_BUCKET)=$" .env)
  if [ -z "$MISSING" ]; then
    echo "✅ .env properly configured"
  else
    echo "❌ .env has empty values"
  fi
else
  echo "❌ .env file not found"
fi
echo ""

# 2. Check dependencies
echo "2️⃣ Checking Python dependencies..."
python -c "import fastapi, openai, firebase_admin, boto3, schedule; print('✅ All core packages available')" 2>/dev/null || echo "❌ Missing dependencies"
echo ""

# 3. Check file structure
echo "3️⃣ Checking project structure..."
REQUIRED_FILES=("src/api_server.py" "src/main.py" "src/agents/analyzer_agent.py" "src/agents/retrain_agent.py" "requirements-minimal.txt")
for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "✅ $file exists"
  else
    echo "❌ $file missing"
  fi
done
echo ""

echo "=============================================="
echo "Verification complete!"
```

---

## 🚀 DEPLOYMENT READINESS MATRIX

| Check | Command | Expected | Status |
|-------|---------|----------|--------|
| **.env validity** | `cat .env` | No empty values | [ ] |
| **Dependencies** | `pip check` | No broken packages | [ ] |
| **API startup** | `uvicorn src.api_server:app` | Runs on :8000 | [ ] |
| **API health** | `curl /health` | 200 OK | [ ] |
| **Predictions** | `python src/main.py` | 8/8 sports success | [ ] |
| **Firestore** | Firebase Console | Documents created | [ ] |
| **S3 upload** | AWS S3 Console | MP3 files uploaded | [ ] |
| **Retraining** | `python src/agents/retrain_agent.py` | Model updated | [ ] |
| **No errors** | Full run | Clean logs | [ ] |

---

## ⚠️ COMMON ISSUES & SOLUTIONS

### Issue: "ModuleNotFoundError: No module named 'openai'"
**Solution:**
```bash
pip install -r requirements-minimal.txt
```

### Issue: "Firebase authentication failed"
**Solution:**
- Verify `firebase-key.json` exists in project root
- Check `FIREBASE_KEY_PATH` in `.env`
- Verify credentials have Firestore write permissions

### Issue: "AWS S3 access denied"
**Solution:**
- Verify AWS credentials in `.env`
- Ensure IAM user has S3 bucket permissions
- Check bucket name matches `AWS_S3_BUCKET`

### Issue: "OpenAI API key invalid"
**Solution:**
- Verify key starts with `sk-`
- Check key hasn't expired
- Confirm API has sufficient quota

### Issue: "Port 8000 already in use"
**Solution:**
```bash
uvicorn src.api_server:app --port 8001
```

---

## ✅ FINAL SIGN-OFF

When all items pass, system is ready for production:

```
✅ Environment configuration verified
✅ All dependencies installed
✅ API server starts successfully
✅ Predictions run end-to-end
✅ Firestore integration working
✅ AWS S3 uploads functional
✅ Auto-retraining operational
✅ No import or runtime errors
✅ Logging system active
✅ Health checks passing

STATUS: READY FOR CLOUD DEPLOYMENT
```

---

## 🎯 DEPLOYMENT COMMANDS

### Local Verification
```bash
# Start API
uvicorn src.api_server:app --reload --port 8000

# In another terminal, test
curl http://localhost:8000/health
curl http://localhost:8000/api/nba
```

### Docker Deployment
```bash
docker build -t rovnic-agent:latest .
docker run -p 8000:8000 -e OPENAI_API_KEY=... rovnic-agent:latest
```

### Cloud Run Deployment
```bash
gcloud run deploy rovnic-agent-api --source . --region us-east1 --allow-unauthenticated
```

---

**Verification Date:** October 28, 2025  
**System:** Rovnic Agentic AI v1.0.0  
**Status:** READY FOR DEPLOYMENT VERIFICATION
