"""
The Odds API integration for fetching real-time odds data.
"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class OddsAPIClient:
    """Fetches real-time odds from The Odds API for 8 sports."""
    
    def __init__(self):
        """Initialize Odds API client."""
        self.api_key = os.getenv("ODDS_API_KEY")
        self.base_url = "https://api.the-odds-api.com/v4"
        self.sports = {
            "nba": "basketball_nba",
            "nfl": "americanfootball_nfl",
            "mlb": "baseball_mlb",
            "nhl": "icehockey_nhl",
            "ncaaf": "americanfootball_ncaaf",
            "ncaab": "basketball_ncaab",
            "soccer": "soccer_epl",
            "ufc": "mma_ufc"
        }
    
    def get_odds(self, sport: str) -> Dict:
        """Fetch live odds for a specific sport."""
        sport_key = self.sports.get(sport.lower())
        if not sport_key:
            logger.error(f"Unknown sport: {sport}")
            return {}
        
        try:
            url = f"{self.base_url}/sports/{sport_key}/odds"
            params = {
                "apiKey": self.api_key,
                "regions": "us",
                "markets": "h2h,spreads,totals"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Fetched odds for {sport}")
                return response.json()
            else:
                logger.error(f"API error for {sport}: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"Error fetching odds for {sport}: {str(e)}")
            return {}
    
    def get_all_sports(self) -> Dict[str, List]:
        """Fetch odds for all supported sports."""
        all_odds = {}
        for sport in self.sports.keys():
            odds = self.get_odds(sport)
            if odds:
                all_odds[sport] = odds
        return all_odds
