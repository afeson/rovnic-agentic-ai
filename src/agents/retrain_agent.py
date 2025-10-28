"""
Model retraining agent for auto-improvement when accuracy drops.
"""

import os
import joblib
from datetime import datetime
from typing import Dict
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import logging
from services.firestore import FirestoreClient

logger = logging.getLogger(__name__)


class RetrainAgent:
    """Automatically retrains models when accuracy threshold is breached."""
    
    def __init__(self):
        """Initialize retrain agent."""
        self.db = FirestoreClient()
        self.model_path = "models/model.pkl"
        self.scaler_path = "models/scaler.pkl"
        self.min_predictions = int(os.getenv("RETRAINING_MIN_PREDICTIONS", 10))
    
    def fetch_recent_predictions(self, sport: str, limit: int = 100) -> pd.DataFrame:
        """Fetch recent predictions from Firestore."""
        try:
            predictions = self.db.get_predictions(sport, "2025-10-28")  # Mock date
            
            if not predictions:
                logger.warning(f"No predictions found for {sport}")
                return pd.DataFrame()
            
            df = pd.DataFrame(predictions)
            logger.info(f"Fetched {len(df)} predictions for {sport}")
            return df
        except Exception as e:
            logger.error(f"Error fetching predictions: {str(e)}")
            return pd.DataFrame()
    
    def prepare_training_data(self, df: pd.DataFrame):
        """Prepare data for model retraining."""
        try:
            if df.empty:
                return None, None
            
            # Mock feature engineering
            features = df[['confidence']].values if 'confidence' in df else np.random.randn(len(df), 1)
            labels = np.array([1 if p == 'Win' else 0 for p in df.get('prediction', [])])
            
            logger.info(f"Prepared {len(features)} training samples")
            return features, labels
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            return None, None
    
    def retrain_model(self, X, y) -> bool:
        """Retrain the ML model."""
        try:
            if X is None or y is None:
                logger.error("No training data")
                return False
            
            logger.info("Starting model retraining...")
            
            # Initialize scaler
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train model
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_scaled, y)
            
            # Save models
            joblib.dump(model, self.model_path)
            joblib.dump(scaler, self.scaler_path)
            
            logger.info("Model retraining completed")
            return True
        except Exception as e:
            logger.error(f"Error retraining model: {str(e)}")
            return False
    
    def validate_model(self, X, y) -> float:
        """Validate retrained model."""
        try:
            model = joblib.load(self.model_path)
            scaler = joblib.load(self.scaler_path)
            
            X_scaled = scaler.transform(X)
            accuracy = model.score(X_scaled, y)
            
            logger.info(f"Model validation accuracy: {accuracy:.2%}")
            return accuracy
        except Exception as e:
            logger.error(f"Error validating model: {str(e)}")
            return 0.0
    
    def trigger_retraining(self, sport: str) -> Dict:
        """Trigger full retraining pipeline."""
        logger.info(f"Triggering retraining for {sport}...")
        
        result = {
            "sport": sport,
            "status": "started",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            # Step 1: Fetch predictions
            logger.info("[1/4] Fetching recent predictions...")
            df = self.fetch_recent_predictions(sport)
            
            if len(df) < self.min_predictions:
                logger.warning(f"Not enough predictions ({len(df)} < {self.min_predictions})")
                result["status"] = "skipped"
                result["reason"] = "Insufficient data"
                return result
            
            # Step 2: Prepare data
            logger.info("[2/4] Preparing training data...")
            X, y = self.prepare_training_data(df)
            
            # Step 3: Retrain
            logger.info("[3/4] Retraining model...")
            if not self.retrain_model(X, y):
                result["status"] = "failed"
                return result
            
            # Step 4: Validate
            logger.info("[4/4] Validating model...")
            accuracy = self.validate_model(X, y)
            
            result["status"] = "completed"
            result["accuracy"] = accuracy
            
            # Save to Firestore
            self.db.save_meta_feedback({
                "sport": sport,
                "retraining_completed": True,
                "new_accuracy": accuracy,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            logger.info(f"Retraining completed for {sport} with accuracy {accuracy:.2%}")
            return result
        except Exception as e:
            logger.error(f"Retraining failed: {str(e)}")
            result["status"] = "failed"
            result["error"] = str(e)
            return result
