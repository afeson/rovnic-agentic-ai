"""
Analyzer Agent - Uses GPT-4.1-mini to analyze predictions intelligently.
"""

import os
import openai
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class AnalyzerAgent:
    """Uses GPT-4.1-mini to analyze predictions."""
    
    def __init__(self):
        """Initialize analyzer agent."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.model = os.getenv("EXPLANATION_MODEL", "gpt-4.1-mini")
    
    def analyze(self, game_data: Dict, prediction: Dict, odds: Dict) -> str:
        """Generate AI analysis for a prediction."""
        if not self.api_key:
            logger.warning("OpenAI API key not set")
            return "Analysis unavailable"
        
        try:
            game = game_data.get('game', 'Game')
            sport = game_data.get('sport', 'Unknown').upper()
            pred = prediction.get('prediction', 'TBD')
            conf = prediction.get('confidence', 0.0)
            
            prompt = f"""
            Analyze this {sport} prediction:
            Game: {game}
            ML Prediction: {pred} (confidence: {conf:.1%})
            
            Provide a 2-3 sentence analysis explaining why this prediction makes sense.
            Focus on: team stats, recent performance, and market factors.
            Keep it concise and actionable.
            """
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content
            logger.info(f"Analysis generated for {game}")
            return analysis
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return "Unable to generate analysis"
