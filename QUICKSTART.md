# ⚡ Quick Start - Rovnic Agentic AI

Get the system running in **5 minutes**.

---

## 1️⃣ Setup (2 minutes)

```bash
# Clone (or navigate to existing directory)
cd rovnic-agentic-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 2️⃣ Configure (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env (add your API keys)
nano .env
```

**Minimum Required:**
```
ODDS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
FIREBASE_KEY_PATH=./firebase-key.json
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_key_here
```

---

## 3️⃣ Add Firebase (1 minute)

```bash
# Download from Firebase Console
# https://console.firebase.google.com → Project Settings → Service Accounts

cp ~/Downloads/firebase-key.json ./firebase-key.json
```

---

## 4️⃣ Run (1 minute)

**Option A: Start API Server**
```bash
uvicorn src.api_server:app --reload --port 8000
```

**Option B: Start Scheduler (4-hour cycles)**
```bash
python src/main.py
```

---

## 5️⃣ Test

**API Server:**
```bash
# Health check
curl http://localhost:8000/health

# NBA predictions
curl http://localhost:8000/api/nba

# Swagger docs
open http://localhost:8000/docs
```

**Expected Response:**
```json
{
  "sport": "NBA",
  "game": "Team A vs Team B",
  "prediction": "Win",
  "confidence": 0.87,
  "analysis": "AI generated analysis...",
  "audio_url": "https://s3.amazonaws.com/...",
  "timestamp": "2025-10-28T15:30:00Z"
}
```

---

## 🎯 Available Endpoints

| Endpoint | Method | Sport |
|----------|--------|-------|
| `/api/nba` | GET | Basketball 🏀 |
| `/api/nfl` | GET | Football 🏈 |
| `/api/mlb` | GET | Baseball ⚾ |
| `/api/nhl` | GET | Hockey 🏒 |
| `/api/ncaaf` | GET | College Football 🏈 |
| `/api/ncaab` | GET | College Basketball 🏀 |
| `/api/soccer` | GET | International Soccer ⚽ |
| `/api/ufc` | GET | MMA 🥊 |

---

## 📊 Check Firestore

1. Go to https://console.firebase.google.com
2. Select your project
3. Navigate to Firestore
4. Check `/predictions/{sport}/{date}/{game_id}`

---

## 🚀 Deploy to Production

### Docker
```bash
docker build -t rovnic-agent:latest .
docker run -p 8000:8000 -e ODDS_API_KEY=... rovnic-agent:latest
```

### Cloud Run (30 seconds)
```bash
gcloud run deploy rovnic-agent-api --source . --region us-east1
```

### Full Guide
See `DEPLOYMENT.md` for comprehensive deployment instructions.

---

## 📱 Frontend Integration

```javascript
// Fetch predictions
const response = await fetch('https://rovnic-agent-api.com/api/nba');
const data = await response.json();

// Display
document.getElementById('prediction').textContent = data.prediction;
document.getElementById('confidence').textContent = `${(data.confidence * 100).toFixed(1)}%`;
document.getElementById('analysis').textContent = data.analysis;

// Play audio
if (data.audio_url) {
  new Audio(data.audio_url).play();
}
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Firestore connection failed"
- Check firebase-key.json exists
- Verify FIREBASE_KEY_PATH in .env

### "API key invalid"
- Check ODDS_API_KEY and OPENAI_API_KEY
- Ensure keys are not expired

### Port 8000 in use
```bash
uvicorn src.api_server:app --port 8001
```

---

## ✅ Success Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env configured with all keys
- [ ] firebase-key.json present
- [ ] API server starts without errors
- [ ] Health check returns 200
- [ ] /api/nba returns prediction
- [ ] Data appears in Firestore

---

## 📚 Next Steps

1. **Production**: See `DEPLOYMENT.md`
2. **Advanced**: See `README.md`
3. **Troubleshooting**: See `README.md` → Troubleshooting
4. **API Docs**: `http://localhost:8000/docs`

---

## 🎉 You're Done!

Your Rovnic Agentic AI is now running and ready to power predictions for all 8 sports.
