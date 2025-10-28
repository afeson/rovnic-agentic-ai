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


if __name__ == "__main__":
    import sys
    
    # Simple test mode
    print("[S3] Testing AWS S3 integration...")
    print("[S3] AWS_ACCESS_KEY_ID:", "SET" if os.getenv("AWS_ACCESS_KEY_ID") else "NOT SET")
    print("[S3] AWS_SECRET_ACCESS_KEY:", "SET" if os.getenv("AWS_SECRET_ACCESS_KEY") else "NOT SET")
    print("[S3] AWS_S3_BUCKET:", os.getenv("AWS_S3_BUCKET", "rovnic-voice-summaries"))
    
    manager = S3Manager()
    
    if manager.s3_client is None:
        print("[S3] ❌ Failed to initialize S3 client")
        print("[S3] Please verify AWS credentials are set in environment variables")
        sys.exit(1)
    
    print("[S3] ✅ S3 client initialized successfully")
    
    # Test list files
    print("[S3] Listing files in bucket...")
    try:
        files = manager.list_files()
        print(f"[S3] ✅ Found {len(files)} files in bucket")
        if files:
            print(f"[S3] Sample files: {files[:5]}")
    except Exception as e:
        print(f"[S3] ❌ Error listing files: {str(e)}")
    
    # Test upload if test file provided
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        print(f"[S3] Testing upload with file: {test_file}")
        
        # Create a test file if it doesn't exist
        if not os.path.exists(test_file):
            print(f"[S3] Creating test file: {test_file}")
            os.makedirs(os.path.dirname(test_file), exist_ok=True)
            with open(test_file, 'wb') as f:
                f.write(b"Test audio data")
        
        # Upload test file
        s3_key = f"test/{os.path.basename(test_file)}"
        url = manager.upload_file(test_file, s3_key)
        
        if url:
            print(f"[S3] ✅ Upload successful!")
            print(f"[S3] File URL: {url}")
        else:
            print(f"[S3] ❌ Upload failed")
            sys.exit(1)
    else:
        print("[S3] ✅ S3 integration test passed!")
        print("[S3] To test file upload, run: python src/services/s3_upload.py output/test.mp3")
