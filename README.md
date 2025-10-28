# 🚀 Rovnic Agentic AI Backend

Enterprise-grade AI prediction system supporting **8 sports** with real-time odds, ML predictions, AI explanations, voice synthesis, and meta-learning.

## 📊 Supported Sports

- 🏀 **NBA** (Basketball)
- 🏈 **NFL** (Football)
- ⚾ **MLB** (Baseball)
- 🏒 **NHL** (Hockey)
- 🏈 **NCAAF** (College Football)
- 🏀 **NCAAB** (College Basketball)
- ⚽ **Soccer** (Global)
- 🥊 **UFC** (Mixed Martial Arts)

---

## 🎯 Features

✅ **Real-Time Odds** - The Odds API integration for live betting lines  
✅ **ML Predictions** - scikit-learn models with confidence scores  
✅ **AI Explanations** - GPT-4.1-mini powered analysis  
✅ **Voice Summaries** - Text-to-speech MP3 generation  
✅ **Cloud Storage** - Firestore + AWS S3 integration  
✅ **Meta-Learning** - Self-improving accuracy tracking  
✅ **Auto-Retraining** - Triggers when accuracy < 80%  
✅ **Audit Logs** - Complete historical record  

---

## 📁 Project Structure

```
rovnic-agentic-ai/
├── src/
│   ├── api_server.py           # FastAPI REST API
│   ├── main.py                 # Scheduler & orchestrator
│   ├── agents/
│   │   ├── analyzer_agent.py   # AI analysis & recommendations
│   │   └── retrain_agent.py    # Model retraining logic
│   ├── services/
│   │   ├── odds_api.py         # The Odds API client
│   │   ├── firestore.py        # Firebase integration
│   │   ├── s3_upload.py        # AWS S3 operations
│   │   ├── tts_engine.py       # Voice synthesis
│   │   ├── ml_pipeline.py      # ML inference
│   │   └── monitor.py          # Accuracy tracking
│   └── utils/
│       └── logger.py           # Logging utility
├── requirements.txt            # Dependencies
├── .env.example               # Environment template
├── Dockerfile                 # Container configuration
├── firebase-key.json          # Firebase credentials (add your own)
└── README.md                  # This file
```

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
cd rovnic-agentic-ai
cp .env.example .env
```

### 2. Add Credentials
```bash
# Edit .env with your keys:
ODDS_API_KEY=your_odds_api_key
OPENAI_API_KEY=your_openai_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

### 3. Add Firebase Key
```bash
# Copy your firebase-key.json to project root
cp ~/path/to/firebase-key.json .
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Locally
```bash
uvicorn src.api_server:app --reload --port 8000
```

### 6. Test Endpoint
```bash
curl http://localhost:8000/api/nba
```

---

## 📡 API Endpoints

All endpoints return structured JSON with predictions, analysis, and voice URLs:

```
GET /api/nba       # Basketball predictions
GET /api/nfl       # Football predictions
GET /api/mlb       # Baseball predictions
GET /api/nhl       # Hockey predictions
GET /api/ncaaf     # College Football
GET /api/ncaab     # College Basketball
GET /api/soccer    # International Soccer
GET /api/ufc       # UFC/MMA

GET /health        # Health check
GET /metrics       # System metrics
```

### Response Format
```json
{
  "sport": "NBA",
  "game": "LAL vs BOS",
  "prediction": "LAL Win",
  "confidence": 0.87,
  "analysis": "Lakers have stronger bench...",
  "audio_url": "https://s3.amazonaws.com/NBA_LAL_BOS.mp3",
  "timestamp": "2025-10-28T15:30:00Z",
  "firestore_path": "predictions/NBA/2025-10-28/LAL_vs_BOS"
}
```

---

## 🧠 System Architecture

### Data Pipeline
```
The Odds API
    ↓
[Fetch Live Odds] → 8 Sports (real-time)
    ↓
[ML Pipeline] → Load model.pkl + scaler.pkl → Predictions
    ↓
[Analyzer Agent] → GPT-4.1-mini → AI Explanations
    ↓
[TTS Engine] → OpenAI TTS → Voice MP3s
    ↓
[Cloud Storage] → Firestore + AWS S3 → Persistence
    ↓
[Monitor] → Accuracy Tracking → Meta-Learning
```

### 4-Hour Refresh Cycle
```
Every 4 hours:
1. Fetch all live games (8 sports)
2. Run ML predictions
3. Generate AI analysis
4. Create voice summaries
5. Store to Firestore/S3
6. Log accuracy metrics
7. Check retraining threshold
8. Auto-retrain if needed
```

---

## 🔧 Service Details

### 1. odds_api.py
Fetches real odds and player props from The Odds API.

```python
from services.odds_api import OddsAPIClient

client = OddsAPIClient(api_key="...")
nba_games = client.get_odds("basketball_nba")
# Returns: [{sport, game, lines, props, odds}...]
```

### 2. ml_pipeline.py
Runs ML predictions on game data.

```python
from services.ml_pipeline import MLPipeline

pipeline = MLPipeline(model_path="models/model.pkl")
predictions = pipeline.predict(game_features)
# Returns: {prediction, confidence, probabilities}
```

### 3. analyzer_agent.py
Uses GPT-4.1-mini for intelligent analysis.

```python
from agents.analyzer_agent import AnalyzerAgent

analyzer = AnalyzerAgent(api_key="...")
analysis = analyzer.analyze(game_data, prediction, odds)
# Returns: AI-generated explanation text
```

### 4. tts_engine.py
Converts text to speech MP3 files.

```python
from services.tts_engine import TTSEngine

tts = TTSEngine(api_key="...", bucket="rovnic-voice")
audio_url = tts.generate_voice(summary_text)
# Returns: S3 URL to MP3 file
```

### 5. firestore.py
Persistent storage in Firebase.

```python
from services.firestore import FirestoreClient

db = FirestoreClient(key_path="firebase-key.json")
db.save_prediction(sport, game_id, prediction_data)
# Saves to: /predictions/{sport}/{date}/{game_id}
```

### 6. monitor.py
Tracks accuracy and triggers retraining.

```python
from services.monitor import AccuracyMonitor

monitor = AccuracyMonitor(db_client)
accuracy = monitor.calculate_rolling_accuracy(days=7)
if accuracy < 0.80:
    trigger_retraining()
```

---

## 🤖 Meta-Learning System

### Automatic Improvement
1. **Accuracy Tracking** - Compares predictions vs actual outcomes
2. **Failure Analysis** - GPT identifies patterns in errors
3. **Suggestions** - AI recommends feature/threshold adjustments
4. **Safe Tuning** - Apply bounded adjustments (±5%)
5. **Retraining** - Trigger model retrain if accuracy < 80%
6. **Audit Logs** - Complete history in Firestore

### Firestore Structure
```
meta_feedback/
├── 2025-10-28/
│   ├── accuracy: 0.87
│   ├── by_sport: {NBA: 0.90, NFL: 0.82}
│   ├── suggestions_applied: 2
│   └── retrain_triggered: false
└── 2025-10-29/
    └── ...
```

---

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t rovnic-agent:latest .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e ODDS_API_KEY=... \
  -e OPENAI_API_KEY=... \
  -v firebase-key.json:/app/firebase-key.json \
  rovnic-agent:latest
```

---

## ☁️ Cloud Deployment

### Google Cloud Run
```bash
gcloud run deploy rovnic-agent-api \
  --source . \
  --region us-east1 \
  --allow-unauthenticated \
  --set-env-vars ODDS_API_KEY=...,OPENAI_API_KEY=...
```

### AWS Lambda
1. Package as zip with dependencies
2. Set handler to `src.api_server.app`
3. Configure environment variables
4. Set timeout to 300 seconds

### AWS EC2
1. Launch Ubuntu instance
2. `git clone` repository
3. `pip install -r requirements.txt`
4. Run with systemd service

---

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy", "timestamp": "..."}
```

### Metrics
```bash
curl http://localhost:8000/metrics
# Response: {predictions: 1250, avg_confidence: 0.82, errors: 3}
```

### Logs
```bash
# Tail logs (Docker)
docker logs -f rovnic-agent

# View logs (File)
tail -f logs/app.log
```

---

## 🔒 Security

✅ API keys stored in `.env` (not committed)  
✅ Firebase credentials in separate JSON file  
✅ AWS credentials via IAM roles (production)  
✅ Input validation on all API endpoints  
✅ Rate limiting on API routes  
✅ CORS configured for rovnic.com  

---

## 🧪 Testing

### Test Single Endpoint
```bash
python -m pytest tests/test_api.py::test_nba_endpoint
```

### Test Services
```bash
python -m pytest tests/test_services.py
```

### Integration Test
```bash
python -m pytest tests/test_integration.py
```

---

## 📈 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Fetch Odds | ~2s | The Odds API |
| ML Prediction | ~1s | Model inference |
| AI Analysis | ~5s | GPT-4.1-mini |
| TTS Generation | ~3s | OpenAI TTS |
| Firestore Save | ~2s | Cloud database |
| **Total** | **~13s** | Per prediction |

---

## 🐛 Troubleshooting

### Issue: "API key invalid"
**Solution:** Check .env file, ensure keys are set correctly

### Issue: "Firebase connection failed"
**Solution:** Verify firebase-key.json exists and path is correct

### Issue: "S3 bucket not found"
**Solution:** Check AWS credentials and bucket name in .env

### Issue: "Model not found"
**Solution:** Ensure models/ directory contains model.pkl and scaler.pkl

---

## 📚 Documentation

- `API_REFERENCE.md` - Detailed endpoint documentation
- `DEPLOYMENT.md` - Cloud deployment guide
- `CONTRIBUTING.md` - Development guidelines
- `ARCHITECTURE.md` - System design details

---

## 🤝 Integration with Rovnic.com

Rovnic.com frontend should request:
```javascript
const response = await fetch('https://rovnic-agent-api.com/api/nba');
const data = await response.json();

// Display prediction
document.getElementById('prediction').textContent = data.prediction;
document.getElementById('confidence').textContent = `${(data.confidence * 100).toFixed(1)}%`;
document.getElementById('analysis').textContent = data.analysis;

// Play audio
new Audio(data.audio_url).play();
```

---

## 🚀 Production Checklist

- [ ] All environment variables configured
- [ ] Firebase key deployed
- [ ] AWS credentials set
- [ ] Models trained and deployed
- [ ] Rate limiting configured
- [ ] CORS configured for rovnic.com
- [ ] SSL certificates installed
- [ ] Monitoring alerts set up
- [ ] Backup strategy configured
- [ ] Load balancer configured

---

## 📞 Support

For issues or questions:
1. Check logs: `tail -f logs/app.log`
2. Review docs: See documentation section
3. Test endpoint: `curl http://localhost:8000/health`
4. Check Firestore: Verify data is being stored

---

## 📄 License

Proprietary - Rovnic.com

---

## 🎉 Ready to Launch!

Your Rovnic Agentic AI backend is production-ready and can power predictions for all 8 sports with real-time odds, AI analysis, and voice summaries.

**Deploy with:** `gcloud run deploy rovnic-agent-api --source .`
