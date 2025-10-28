"""
AWS S3 operations for storing voice summaries and audio files.
"""

import os
import boto3
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class S3Manager:
    """Manages AWS S3 operations for audio files."""
    
    def __init__(self):
        """Initialize S3 client."""
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name='us-east-1'
            )
            self.bucket = os.getenv("AWS_S3_BUCKET", "rovnic-voice-summaries")
            logger.info("S3 client initialized")
        except Exception as e:
            logger.error(f"S3 initialization error: {str(e)}")
            self.s3_client = None
    
    def upload_file(self, file_path: str, s3_key: str) -> Optional[str]:
        """Upload file to S3 and return public URL."""
        if self.s3_client is None:
            logger.error("S3 client not initialized")
            return None
        
        try:
            self.s3_client.upload_file(
                file_path,
                self.bucket,
                s3_key,
                ExtraArgs={'ContentType': 'audio/mpeg', 'ACL': 'public-read'}
            )
            
            url = f"https://{self.bucket}.s3.amazonaws.com/{s3_key}"
            logger.info(f"File uploaded: {url}")
            return url
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            return None
    
    def upload_bytes(self, file_bytes: bytes, s3_key: str) -> Optional[str]:
        """Upload bytes to S3."""
        if self.s3_client is None:
            return None
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=file_bytes,
                ContentType='audio/mpeg',
                ACL='public-read'
            )
            
            url = f"https://{self.bucket}.s3.amazonaws.com/{s3_key}"
            logger.info(f"Bytes uploaded: {url}")
            return url
        except Exception as e:
            logger.error(f"Error uploading bytes: {str(e)}")
            return None
    
    def delete_file(self, s3_key: str) -> bool:
        """Delete file from S3."""
        if self.s3_client is None:
            return False
        
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=s3_key)
            logger.info(f"File deleted: {s3_key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    def list_files(self, prefix: str = "") -> list:
        """List files in S3 bucket."""
        if self.s3_client is None:
            return []
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix
            )
            
            files = []
            if 'Contents' in response:
                files = [obj['Key'] for obj in response['Contents']]
            
            logger.info(f"Listed {len(files)} files")
            return files
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return []
