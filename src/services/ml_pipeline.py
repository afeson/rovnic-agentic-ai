"""
ML Pipeline - Load and run predictions using trained models.
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class MLPipeline:
    """Loads and runs ML predictions."""
    
    def __init__(self, model_path: str = "models/model.pkl"):
        """Initialize ML pipeline."""
        self.model_path = Path(model_path)
        self.scaler_path = self.model_path.parent / "scaler.pkl"
        self.model = None
        self.scaler = None
        self._load_models()
    
    def _load_models(self):
        """Load trained model and scaler."""
        try:
            if self.model_path.exists():
                self.model = joblib.load(self.model_path)
                logger.info("Model loaded successfully")
            else:
                logger.warning(f"Model not found at {self.model_path}")
            
            if self.scaler_path.exists():
                self.scaler = joblib.load(self.scaler_path)
                logger.info("Scaler loaded successfully")
            else:
                logger.warning(f"Scaler not found at {self.scaler_path}")
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
    
    def predict(self, features: list) -> Dict:
        """Generate prediction with confidence."""
        if self.model is None or self.scaler is None:
            logger.warning("Models not available, returning mock prediction")
            return {
                "prediction": "Win",
                "confidence": 0.75,
                "probability": {"lose": 0.25, "win": 0.75}
            }
        
        try:
            X = self.scaler.transform([features])
            proba = self.model.predict_proba(X)[0]
            
            return {
                "prediction": "Win" if proba[1] > 0.5 else "Loss",
                "confidence": float(proba[1]),
                "probability": {"lose": float(proba[0]), "win": float(proba[1])}
            }
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {"error": str(e)}
