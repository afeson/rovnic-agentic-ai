"""
TTS Engine - Convert text to speech and upload to S3.
"""

import os
import openai
import boto3
import uuid
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TTSEngine:
    """Generates voice summaries and uploads to S3."""
    
    def __init__(self):
        """Initialize TTS engine."""
        try:
            self.api_key = os.getenv("OPENAI_API_KEY")
            openai.api_key = self.api_key
            
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name='us-east-1'
            )
            self.bucket = os.getenv("AWS_S3_BUCKET", "rovnic-voice-summaries")
            logger.info("TTS engine initialized")
        except Exception as e:
            logger.error(f"TTS initialization error: {str(e)}")
            self.s3_client = None
    
    def generate_voice(self, text: str, sport: str) -> Optional[str]:
        """Generate voice from text and upload to S3."""
        if not text or not self.api_key:
            logger.warning("Missing text or API key")
            return None
        
        try:
            # Generate speech
            logger.info(f"Generating voice for {sport}...")
            response = openai.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text[:500]  # Limit to 500 chars
            )
            
            # Upload to S3
            if self.s3_client:
                file_key = f"{sport.lower()}/{uuid.uuid4().hex[:8]}.mp3"
                self.s3_client.put_object(
                    Bucket=self.bucket,
                    Key=file_key,
                    Body=response.content,
                    ContentType="audio/mpeg",
                    ACL="public-read"
                )
                
                url = f"https://{self.bucket}.s3.amazonaws.com/{file_key}"
                logger.info(f"Voice generated and uploaded: {url}")
                return url
            else:
                logger.warning("S3 client not available")
                return None
                
        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            return None
