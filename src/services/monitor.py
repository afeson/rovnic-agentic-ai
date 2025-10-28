"""
Accuracy monitoring and meta-learning system.
"""

import os
from datetime import datetime, timedelta
from typing import Dict
import logging
from services.firestore import FirestoreClient

logger = logging.getLogger(__name__)


class AccuracyMonitor:
    """Monitors prediction accuracy and triggers retraining."""
    
    def __init__(self):
        """Initialize monitor."""
        self.db = FirestoreClient()
        self.accuracy_threshold = float(os.getenv("ACCURACY_THRESHOLD", 0.80))
        self.rolling_window = int(os.getenv("ROLLING_WINDOW_DAYS", 7))
    
    def calculate_rolling_accuracy(self, sport: str) -> float:
        """Calculate rolling accuracy for a sport."""
        try:
            accuracy = self.db.calculate_accuracy(sport, self.rolling_window)
            logger.info(f"Rolling accuracy for {sport}: {accuracy:.2%}")
            return accuracy
        except Exception as e:
            logger.error(f"Error calculating accuracy: {str(e)}")
            return 0.0
    
    def check_retraining_needed(self, sport: str) -> bool:
        """Check if retraining is needed."""
        accuracy = self.calculate_rolling_accuracy(sport)
        
        if accuracy < self.accuracy_threshold:
            logger.warning(f"Retraining needed for {sport}: accuracy {accuracy:.2%} < {self.accuracy_threshold:.2%}")
            return True
        
        logger.info(f"No retraining needed for {sport}")
        return False
    
    def save_accuracy_log(self, sport: str, accuracy: float) -> bool:
        """Save accuracy metrics to Firestore."""
        try:
            log_data = {
                "sport": sport,
                "accuracy": accuracy,
                "timestamp": datetime.utcnow().isoformat(),
                "threshold_met": accuracy >= self.accuracy_threshold
            }
            
            return self.db.save_meta_feedback(log_data)
        except Exception as e:
            logger.error(f"Error saving accuracy log: {str(e)}")
            return False
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary for all sports."""
        sports = ["nba", "nfl", "mlb", "nhl", "ncaaf", "ncaab", "soccer", "ufc"]
        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "sports": {}
        }
        
        for sport in sports:
            accuracy = self.calculate_rolling_accuracy(sport)
            summary["sports"][sport] = {
                "accuracy": accuracy,
                "needs_retraining": accuracy < self.accuracy_threshold
            }
        
        return summary
