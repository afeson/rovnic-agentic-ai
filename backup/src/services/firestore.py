"""
Firestore integration for storing predictions and meta-learning logs.
"""

import os
from datetime import datetime
from typing import Dict, Optional
import firebase_admin
from firebase_admin import credentials, firestore
import logging

logger = logging.getLogger(__name__)


class FirestoreClient:
    """Manages Firestore operations for predictions and audit logs."""
    
    def __init__(self, key_path: Optional[str] = None):
        """Initialize Firestore client."""
        if key_path is None:
            key_path = os.getenv("FIREBASE_KEY_PATH", "./firebase-key.json")
        
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(key_path)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            logger.info("Firestore client initialized")
        except Exception as e:
            logger.error(f"Firestore initialization error: {str(e)}")
            self.db = None
    
    def save_prediction(self, sport: str, prediction_data: Dict) -> bool:
        """Save prediction to Firestore."""
        if self.db is None:
            logger.error("Firestore not initialized")
            return False
        
        try:
            today = datetime.utcnow().date().isoformat()
            game_id = prediction_data.get("game", "unknown").replace(" ", "_")
            
            # Path: predictions/{sport}/{date}/{game_id}
            path = f"predictions/{sport}/{today}/{game_id}"
            
            data = {
                **prediction_data,
                "timestamp": datetime.utcnow().isoformat(),
                "sport": sport.upper()
            }
            
            self.db.document(path).set(data)
            logger.info(f"Prediction saved: {path}")
            return True
        except Exception as e:
            logger.error(f"Error saving prediction: {str(e)}")
            return False
    
    def get_predictions(self, sport: str, date: str) -> list:
        """Fetch predictions for a sport on a specific date."""
        if self.db is None:
            return []
        
        try:
            path = f"predictions/{sport}/{date}"
            docs = self.db.collection_group("predictions").where(
                "sport", "==", sport.upper()
            ).where(
                "timestamp", ">=", f"{date}T00:00:00"
            ).where(
                "timestamp", "<", f"{date}T23:59:59"
            ).stream()
            
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            logger.error(f"Error fetching predictions: {str(e)}")
            return []
    
    def save_meta_feedback(self, feedback_data: Dict) -> bool:
        """Save meta-learning feedback."""
        if self.db is None:
            return False
        
        try:
            today = datetime.utcnow().date().isoformat()
            path = f"meta_feedback/{today}"
            
            data = {
                **feedback_data,
                "timestamp": datetime.utcnow().isoformat(),
                "date": today
            }
            
            self.db.document(path).set(data, merge=True)
            logger.info(f"Meta feedback saved: {path}")
            return True
        except Exception as e:
            logger.error(f"Error saving meta feedback: {str(e)}")
            return False
    
    def get_meta_feedback(self, days: int = 7) -> list:
        """Fetch recent meta-learning feedback."""
        if self.db is None:
            return []
        
        try:
            docs = self.db.collection("meta_feedback").order_by(
                "timestamp", direction=firestore.Query.DESCENDING
            ).limit(days).stream()
            
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            logger.error(f"Error fetching meta feedback: {str(e)}")
            return []
    
    def calculate_accuracy(self, sport: str, days: int = 7) -> float:
        """Calculate rolling accuracy for a sport."""
        if self.db is None:
            return 0.0
        
        try:
            # Query recent predictions
            docs = self.db.collection_group("predictions").where(
                "sport", "==", sport.upper()
            ).limit(100).stream()
            
            predictions = [doc.to_dict() for doc in docs]
            
            if not predictions:
                return 0.0
            
            # Calculate accuracy (mock - would compare with actual outcomes)
            correct = sum(1 for p in predictions if p.get("correct", False))
            total = len(predictions)
            
            accuracy = correct / total if total > 0 else 0.0
            logger.info(f"Accuracy for {sport}: {accuracy:.2%}")
            
            return accuracy
        except Exception as e:
            logger.error(f"Error calculating accuracy: {str(e)}")
            return 0.0
