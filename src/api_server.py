"""
FastAPI REST API server for Rovnic Agentic AI.
Exposes endpoints for all 8 supported sports.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
import os
import logging
from dotenv import load_dotenv

# Setup
load_dotenv()

# Create logger
logger = logging.getLogger("rovnic_api")
logger.setLevel(logging.INFO)

# FastAPI app
app = FastAPI(
    title="Rovnic Agentic AI",
    description="Enterprise AI prediction system for 8 sports",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to initialize services, fail gracefully if dependencies missing
try:
    from utils.logger import setup_logging
    logger = setup_logging("rovnic_api")
except Exception as e:
    logger.warning(f"Could not load setup_logging: {e}")

try:
    from services.odds_api import OddsAPIClient
    odds_client = OddsAPIClient()
except Exception as e:
    logger.warning(f"Could not load OddsAPIClient: {e}")
    odds_client = None

try:
    from services.ml_pipeline import MLPipeline
    ml_pipeline = MLPipeline()
except Exception as e:
    logger.warning(f"Could not load MLPipeline: {e}")
    ml_pipeline = None

try:
    from services.firestore import FirestoreClient
    db = FirestoreClient()
except Exception as e:
    logger.warning(f"Could not load FirestoreClient: {e}")
    db = None

try:
    from services.s3_upload import S3Manager
    s3_manager = S3Manager()
except Exception as e:
    logger.warning(f"Could not load S3Manager: {e}")
    s3_manager = None

try:
    from services.monitor import AccuracyMonitor
    monitor = AccuracyMonitor()
except Exception as e:
    logger.warning(f"Could not load AccuracyMonitor: {e}")
    monitor = None

try:
    from agents.analyzer_agent import AnalyzerAgent
    analyzer = AnalyzerAgent()
except Exception as e:
    logger.warning(f"Could not load AnalyzerAgent: {e}")
    analyzer = None

try:
    from agents.retrain_agent import RetrainAgent
    retrain_agent = RetrainAgent()
except Exception as e:
    logger.warning(f"Could not load RetrainAgent: {e}")
    retrain_agent = None

# Models
class PredictionResponse(BaseModel):
    sport: str
    game: str
    prediction: str
    confidence: float
    analysis: str
    audio_url: Optional[str]
    timestamp: str
    firestore_path: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str


class MetricsResponse(BaseModel):
    predictions_total: int
    avg_confidence: float
    errors: int


# Global stats
class Stats:
    predictions_total = 0
    avg_confidence = 0.0
    errors = 0


stats = Stats()


# Health endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    logger.info("[HEALTH] Health check")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get system metrics."""
    logger.info("[METRICS] Retrieving metrics")
    return {
        "predictions_total": stats.predictions_total,
        "avg_confidence": stats.avg_confidence,
        "errors": stats.errors
    }


# Root and simple endpoints
@app.get("/")
async def root():
    """Root endpoint - API status."""
    logger.info("[ROOT] Root endpoint accessed")
    return {
        "status": "ok",
        "message": "Rovnic Agentic AI API is live!",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/predict")
async def predict():
    """Simple prediction endpoint."""
    logger.info("[PREDICT] Simple prediction endpoint called")
    try:
        if ml_pipeline is None:
            return {
                "prediction": "Win",
                "confidence": 0.75,
                "status": "using_default_model"
            }
        
        # Generate prediction using ML pipeline
        features = [0.5, 1.2]  # Mock features
        result = ml_pipeline.predict(features)
        logger.info(f"[PREDICT] Prediction generated: {result}")
        return result
    except Exception as e:
        logger.error(f"[PREDICT] Error: {str(e)}")
        return {
            "prediction": "Unable to predict",
            "confidence": 0.0,
            "error": str(e)
        }


@app.get("/odds")
async def odds():
    """Get live odds data."""
    logger.info("[ODDS] Live odds endpoint called")
    try:
        if odds_client is None:
            return {
                "odds": [],
                "status": "odds_client_unavailable"
            }
        
        # Fetch odds for NBA as default
        odds_data = odds_client.get_odds("nba")
        logger.info(f"[ODDS] Fetched odds data")
        return {
            "odds": odds_data,
            "sport": "nba",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"[ODDS] Error: {str(e)}")
        return {
            "odds": [],
            "error": str(e)
        }


# Sport prediction endpoints
async def predict_sport(sport: str, background_tasks: BackgroundTasks) -> PredictionResponse:
    """Generic sport prediction handler."""
    logger.info(f"[API] Prediction request for {sport.upper()}")
    
    try:
        # 1. Fetch odds
        logger.info(f"[FETCH] Fetching live odds for {sport}...")
        odds_data = odds_client.get_odds(sport)
        
        if not odds_data:
            stats.errors += 1
            logger.warning(f"No odds data for {sport}")
            raise HTTPException(
                status_code=404,
                detail=f"No games available for {sport}"
            )
        
        # 2. ML prediction
        logger.info(f"[PREDICT] Running ML for {sport}...")
        features = [0.5, 1.2]  # Mock - extract from odds_data in production
        prediction = ml_pipeline.predict(features)
        
        if "error" in prediction:
            stats.errors += 1
            raise HTTPException(status_code=500, detail="Prediction failed")
        
        # 3. AI analysis
        logger.info(f"[ANALYZE] AI analysis for {sport}...")
        game_data = {"game": "Team A vs Team B", "sport": sport}
        analysis = analyzer.analyze(game_data, prediction, odds_data)
        
        # 4. Generate voice (mock - would integrate TTS here)
        audio_url = None
        
        # 5. Build response
        today = datetime.utcnow().date().isoformat()
        game_id = "game_1"
        firestore_path = f"predictions/{sport.upper()}/{today}/{game_id}"
        
        result = {
            "sport": sport.upper(),
            "game": "Team A vs Team B",
            "prediction": prediction.get("prediction"),
            "confidence": prediction.get("confidence"),
            "analysis": analysis,
            "audio_url": audio_url,
            "timestamp": datetime.utcnow().isoformat(),
            "firestore_path": firestore_path
        }
        
        # 6. Save to Firestore (background)
        background_tasks.add_task(db.save_prediction, sport, result)
        
        # Update stats
        stats.predictions_total += 1
        stats.avg_confidence = (
            (stats.avg_confidence * (stats.predictions_total - 1) + prediction.get("confidence")) 
            / stats.predictions_total
        )
        
        logger.info(f"[SUCCESS] {sport.upper()} prediction returned")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        stats.errors += 1
        logger.error(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# API Endpoints for 8 Sports
@app.get("/api/nba", response_model=PredictionResponse)
async def get_nba(background_tasks: BackgroundTasks):
    """NBA predictions."""
    return await predict_sport("nba", background_tasks)


@app.get("/api/nfl", response_model=PredictionResponse)
async def get_nfl(background_tasks: BackgroundTasks):
    """NFL predictions."""
    return await predict_sport("nfl", background_tasks)


@app.get("/api/mlb", response_model=PredictionResponse)
async def get_mlb(background_tasks: BackgroundTasks):
    """MLB predictions."""
    return await predict_sport("mlb", background_tasks)


@app.get("/api/nhl", response_model=PredictionResponse)
async def get_nhl(background_tasks: BackgroundTasks):
    """NHL predictions."""
    return await predict_sport("nhl", background_tasks)


@app.get("/api/ncaaf", response_model=PredictionResponse)
async def get_ncaaf(background_tasks: BackgroundTasks):
    """NCAAF predictions."""
    return await predict_sport("ncaaf", background_tasks)


@app.get("/api/ncaab", response_model=PredictionResponse)
async def get_ncaab(background_tasks: BackgroundTasks):
    """NCAAB predictions."""
    return await predict_sport("ncaab", background_tasks)


@app.get("/api/soccer", response_model=PredictionResponse)
async def get_soccer(background_tasks: BackgroundTasks):
    """Soccer predictions."""
    return await predict_sport("soccer", background_tasks)


@app.get("/api/ufc", response_model=PredictionResponse)
async def get_ufc(background_tasks: BackgroundTasks):
    """UFC predictions."""
    return await predict_sport("ufc", background_tasks)


# Admin endpoints
@app.get("/admin/accuracy")
async def get_accuracy_summary():
    """Get accuracy summary for all sports."""
    logger.info("[ADMIN] Accuracy summary requested")
    return monitor.get_performance_summary()


@app.post("/admin/retrain/{sport}")
async def trigger_retrain(sport: str):
    """Manually trigger retraining for a sport."""
    logger.info(f"[ADMIN] Retraining triggered for {sport}")
    result = retrain_agent.trigger_retraining(sport)
    return result


@app.get("/admin/meta-feedback")
async def get_meta_feedback(days: int = 7):
    """Get meta-learning feedback history."""
    logger.info("[ADMIN] Meta-feedback requested")
    return db.get_meta_feedback(days)


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("[STARTUP] Rovnic Agentic AI API Server")
    logger.info("=" * 60)
    logger.info(f"[CONFIG] Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"[CONFIG] Accuracy Threshold: {os.getenv('ACCURACY_THRESHOLD', 0.80)}")
    logger.info(f"[CONFIG] Port: {os.getenv('PORT', 8000)}")
    logger.info("=" * 60 + "\n")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("[SHUTDOWN] API Server shutting down")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
