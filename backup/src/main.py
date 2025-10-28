"""
Main orchestrator for Rovnic Agentic AI 4-hour prediction cycle.
"""

import os
import schedule
import time
from datetime import datetime
from typing import List
import logging
from dotenv import load_dotenv

from utils.logger import setup_logging
from services.odds_api import OddsAPIClient
from services.ml_pipeline import MLPipeline
from services.firestore import FirestoreClient
from services.s3_upload import S3Manager
from services.monitor import AccuracyMonitor
from agents.analyzer_agent import AnalyzerAgent
from agents.retrain_agent import RetrainAgent

# Setup logging
logger = setup_logging("rovnic_main")

# Load environment
load_dotenv()

# Initialize services
odds_client = OddsAPIClient()
ml_pipeline = MLPipeline()
analyzer = AnalyzerAgent()
s3_manager = S3Manager()
db = FirestoreClient()
monitor = AccuracyMonitor()
retrain_agent = RetrainAgent()

# All supported sports
SPORTS = ["nba", "nfl", "mlb", "nhl", "ncaaf", "ncaab", "soccer", "ufc"]


def process_sport(sport: str) -> bool:
    """Process predictions for a single sport."""
    logger.info(f"[PROCESS] Starting {sport.upper()}...")
    
    try:
        # 1. Fetch live odds
        logger.info(f"[FETCH] Getting live odds for {sport}...")
        odds_data = odds_client.get_odds(sport)
        if not odds_data:
            logger.warning(f"No odds data for {sport}")
            return False
        
        # 2. Run ML prediction
        logger.info(f"[PREDICT] Running ML predictions for {sport}...")
        features = [0.5, 1.2]  # Mock - extract from odds_data in production
        prediction = ml_pipeline.predict(features)
        
        # 3. AI analysis
        logger.info(f"[ANALYZE] Generating AI analysis for {sport}...")
        game_data = {"game": "Team A vs Team B", "sport": sport}
        analysis = analyzer.analyze(game_data, prediction, odds_data)
        
        # 4. Generate voice
        logger.info(f"[VOICE] Generating voice summary for {sport}...")
        summary_text = f"Prediction: {prediction.get('prediction')} with {prediction.get('confidence'):.1%} confidence. {analysis}"
        audio_url = None  # Mock TTS
        
        # 5. Save to Firestore
        logger.info(f"[SAVE] Saving to Firestore for {sport}...")
        result = {
            "sport": sport.upper(),
            "game": "Team A vs Team B",
            "prediction": prediction.get("prediction"),
            "confidence": prediction.get("confidence"),
            "analysis": analysis,
            "audio_url": audio_url,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        db.save_prediction(sport, result)
        logger.info(f"[SUCCESS] {sport.upper()} predictions saved")
        return True
        
    except Exception as e:
        logger.error(f"[ERROR] Error processing {sport}: {str(e)}")
        return False


def run_prediction_cycle():
    """Run complete prediction cycle for all sports."""
    logger.info("=" * 60)
    logger.info(f"[CYCLE] Starting 4-hour prediction cycle at {datetime.utcnow()}")
    logger.info("=" * 60)
    
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "sports": {},
        "summary": {}
    }
    
    # Process each sport
    successful = 0
    for sport in SPORTS:
        success = process_sport(sport)
        results["sports"][sport] = {"success": success}
        if success:
            successful += 1
    
    # Check accuracy and retraining
    logger.info("[MONITOR] Checking accuracy metrics...")
    for sport in SPORTS:
        accuracy = monitor.calculate_rolling_accuracy(sport)
        logger.info(f"[ACCURACY] {sport.upper()}: {accuracy:.2%}")
        
        if monitor.check_retraining_needed(sport):
            logger.warning(f"[RETRAIN] Triggering retraining for {sport}...")
            retrain_result = retrain_agent.trigger_retraining(sport)
            logger.info(f"[RETRAIN] Result: {retrain_result}")
    
    results["summary"] = {
        "total_sports": len(SPORTS),
        "successful": successful,
        "failed": len(SPORTS) - successful
    }
    
    logger.info("=" * 60)
    logger.info(f"[CYCLE] Cycle complete: {successful}/{len(SPORTS)} successful")
    logger.info("=" * 60)
    
    return results


def schedule_predictions():
    """Schedule the prediction cycle."""
    refresh_hours = int(os.getenv("REFRESH_INTERVAL_HOURS", 4))
    logger.info(f"[SCHEDULER] Scheduling predictions every {refresh_hours} hours")
    
    # Run immediately on start
    run_prediction_cycle()
    
    # Schedule recurring
    schedule.every(refresh_hours).hours.do(run_prediction_cycle)
    
    # Keep scheduler running
    logger.info("[SCHEDULER] Prediction scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(60)


def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("[STARTUP] Rovnic Agentic AI Backend")
    logger.info("=" * 60)
    logger.info(f"[CONFIG] Supported Sports: {', '.join(SPORTS)}")
    logger.info(f"[CONFIG] Refresh Interval: {os.getenv('REFRESH_INTERVAL_HOURS', 4)} hours")
    logger.info(f"[CONFIG] Accuracy Threshold: {os.getenv('ACCURACY_THRESHOLD', 0.80)}")
    logger.info("=" * 60 + "\n")
    
    try:
        schedule_predictions()
    except KeyboardInterrupt:
        logger.info("[SHUTDOWN] Shutting down...")
    except Exception as e:
        logger.error(f"[FATAL] {str(e)}")


if __name__ == "__main__":
    main()
