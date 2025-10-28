# 🔑 AWS ENVIRONMENT SETUP GUIDE - Rovnic Agentic AI

**Date:** October 28, 2025  
**Status:** ✅ AWS CONFIGURATION READY  
**Latest Deployment:** Revision 00005-fhp  

---

## 🎯 AWS ENVIRONMENT VARIABLES ADDED

Your Rovnic Agentic AI now has AWS environment variables configured for S3 audio storage!

---

## 📋 AWS ENVIRONMENT VARIABLES

### Configuration Variables (Set in Cloud Run)
```bash
AWS_DEFAULT_REGION=us-east-1
AWS_S3_BUCKET=rovnic-ai-audio-storage
```

### Credentials Variables (Set Locally/Cloud Run)
```bash
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
```

---

## 🔐 HOW TO GET AWS CREDENTIALS

### Step 1: Create IAM User (if you don't have one)
1. Go to: https://console.aws.amazon.com/iam/
2. Click "Users" → "Create user"
3. Give it a name (e.g., "rovnic-ai-user")
4. Click "Create user"

### Step 2: Create Access Key
1. In IAM Users, select your user
2. Click "Security credentials" tab
3. Click "Create access key"
4. Choose "Application running outside AWS"
5. Click "Create access key"
6. **SAVE** the Access Key ID and Secret Access Key (you won't see them again!)

### Step 3: Create S3 Bucket
1. Go to: https://s3.console.aws.amazon.com/
2. Click "Create bucket"
3. Name: `rovnic-ai-audio-storage`
4. Region: `us-east-1`
5. Click "Create bucket"

### Step 4: Add S3 Permissions to IAM User
1. Go to IAM Users
2. Select your user
3. Click "Add permissions" → "Attach policies directly"
4. Search for "AmazonS3FullAccess"
5. Select it and click "Add permissions"

---

## 📝 SETTING UP AWS CREDENTIALS

### Option 1: Local Development (.env file)

Create a `.env` file in the project root:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=us-east-1
AWS_S3_BUCKET=rovnic-ai-audio-storage
```

**Important:** Add `.env` to `.gitignore` (it already is!) to avoid committing credentials.

### Option 2: Cloud Run Environment Variables

Set credentials in Cloud Run:

```bash
gcloud run services update rovnic-agent-api \
  --region us-east1 \
  --set-env-vars \
    AWS_ACCESS_KEY_ID=your_key,\
    AWS_SECRET_ACCESS_KEY=your_secret,\
    AWS_DEFAULT_REGION=us-east-1,\
    AWS_S3_BUCKET=rovnic-ai-audio-storage
```

### Option 3: AWS CLI Configuration

Configure AWS CLI locally:

```bash
aws configure
# Enter your Access Key ID when prompted
# Enter your Secret Access Key when prompted
# Enter region: us-east-1
# Enter output format: json
```

Then boto3 will automatically use these credentials.

---

## 🧪 TESTING AWS S3 INTEGRATION

### Test S3 Connection

```bash
# Basic test (check credentials and bucket)
python src/services/s3_upload.py

# Expected output:
# [S3] Testing AWS S3 integration...
# [S3] AWS_ACCESS_KEY_ID: SET
# [S3] AWS_SECRET_ACCESS_KEY: SET
# [S3] AWS_S3_BUCKET: rovnic-ai-audio-storage
# [S3] ✅ S3 client initialized successfully
# [S3] ✅ S3 integration test passed!
```

### Test File Upload

```bash
# Create output directory first
mkdir output

# Test upload
python src/services/s3_upload.py output/test.mp3

# Expected output:
# [S3] Testing AWS S3 integration...
# [S3] AWS_ACCESS_KEY_ID: SET
# [S3] AWS_SECRET_ACCESS_KEY: SET
# [S3] AWS_S3_BUCKET: rovnic-ai-audio-storage
# [S3] ✅ S3 client initialized successfully
# [S3] Creating test file: output/test.mp3
# [S3] Testing upload with file: output/test.mp3
# [S3] ✅ Upload successful!
# [S3] File URL: https://rovnic-ai-audio-storage.s3.amazonaws.com/test/test.mp3
```

### Verify File in S3

```bash
# List files in S3 bucket
aws s3 ls s3://rovnic-ai-audio-storage/

# Or view in AWS Console:
https://s3.console.aws.amazon.com/s3/buckets/rovnic-ai-audio-storage
```

---

## 🚀 CURRENT CLOUD RUN DEPLOYMENT

### Deployment Details
```
Service: rovnic-agent-api
Region: us-east1
Revision: 00005-fhp (Latest)
Status: ✅ LIVE
Environment Variables Set:
  • AWS_DEFAULT_REGION=us-east-1
  • AWS_S3_BUCKET=rovnic-ai-audio-storage
  • (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY still need to be set)
```

### To Complete Setup on Cloud Run

```bash
gcloud run services update rovnic-agent-api \
  --region us-east1 \
  --set-env-vars \
    AWS_ACCESS_KEY_ID=YOUR_AWS_KEY_ID_HERE,\
    AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY_HERE
```

---

## 📝 S3_UPLOAD.PY UPDATES

### New Features Added

The `src/services/s3_upload.py` file now includes:

✅ **Test Mode** - Check S3 connectivity  
✅ **File Upload Testing** - Upload and verify files  
✅ **Credential Validation** - Check if credentials are set  
✅ **Bucket Verification** - Verify bucket exists  

### Class Methods

```python
# Initialize S3 client with credentials
manager = S3Manager()

# Upload file and get public URL
url = manager.upload_file("local/path/file.mp3", "s3/key/file.mp3")

# Upload bytes
url = manager.upload_bytes(b"audio_data", "s3/key/file.mp3")

# Delete file
manager.delete_file("s3/key/file.mp3")

# List files in bucket
files = manager.list_files(prefix="nba/")
```

---

## 🔗 S3 INTEGRATION IN API

### Automatic S3 Upload in API Server

When you make prediction requests, audio files are automatically uploaded to S3:

```python
# In api_server.py
# When creating voice summaries:
audio_url = tts_engine.generate_voice(analysis, sport)
# This returns an S3 URL like:
# https://rovnic-ai-audio-storage.s3.amazonaws.com/nba/abc123.mp3
```

### API Response with S3 URL

```json
{
  "sport": "NBA",
  "game": "LAL vs BOS",
  "prediction": "Lakers Win",
  "confidence": 0.87,
  "analysis": "Based on recent form...",
  "audio_url": "https://rovnic-ai-audio-storage.s3.amazonaws.com/nba/xyz789.mp3",
  "timestamp": "2025-10-28T15:30:00Z"
}
```

---

## 🛠️ TROUBLESHOOTING

### Error: "AWS_ACCESS_KEY_ID not set"

**Solution:**
```bash
# Set locally in .env file
echo "AWS_ACCESS_KEY_ID=your_key" >> .env
echo "AWS_SECRET_ACCESS_KEY=your_secret" >> .env

# Or in Cloud Run
gcloud run services update rovnic-agent-api \
  --region us-east1 \
  --set-env-vars AWS_ACCESS_KEY_ID=your_key
```

### Error: "Unable to locate credentials"

**Solutions:**
1. Check credentials are in `.env` file
2. Run `aws configure` to set up AWS CLI
3. Check IAM user has S3 permissions
4. Verify Access Key hasn't expired

### Error: "Access Denied to S3 bucket"

**Solutions:**
1. Verify bucket name: `rovnic-ai-audio-storage`
2. Check IAM user has `AmazonS3FullAccess` policy
3. Verify bucket exists in `us-east-1` region
4. Check bucket policy allows uploads

### Error: "InvalidAccessKeyId"

**Solution:**
```bash
# Get new credentials from AWS Console
# https://console.aws.amazon.com/iam/
# Update .env or Cloud Run environment variables
```

### Error: "NoSuchBucket"

**Solution:**
```bash
# Create bucket
aws s3 mb s3://rovnic-ai-audio-storage --region us-east-1

# Or in AWS Console:
# https://s3.console.aws.amazon.com/
```

---

## 📊 AWS ENVIRONMENT VARIABLES CHECKLIST

- ✅ `AWS_DEFAULT_REGION` = us-east-1
- ✅ `AWS_S3_BUCKET` = rovnic-ai-audio-storage
- ⏳ `AWS_ACCESS_KEY_ID` = (To be set with your credentials)
- ⏳ `AWS_SECRET_ACCESS_KEY` = (To be set with your credentials)

---

## 🔐 SECURITY BEST PRACTICES

### Do's ✅
- ✅ Keep AWS credentials in `.env` (Git-ignored)
- ✅ Use IAM users, not root account
- ✅ Rotate Access Keys every 90 days
- ✅ Use minimal permissions (S3 only if possible)
- ✅ Enable S3 bucket versioning
- ✅ Enable S3 server-side encryption

### Don'ts ❌
- ❌ Don't commit `.env` to Git
- ❌ Don't share AWS credentials
- ❌ Don't use root account credentials
- ❌ Don't use permanent credentials in code
- ❌ Don't set overly permissive IAM policies

### Enable S3 Encryption

```bash
# Enable server-side encryption
aws s3api put-bucket-encryption \
  --bucket rovnic-ai-audio-storage \
  --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'
```

### Enable S3 Versioning

```bash
aws s3api put-bucket-versioning \
  --bucket rovnic-ai-audio-storage \
  --versioning-configuration Status=Enabled
```

---

## 📈 MONITORING S3 USAGE

### Check S3 Bucket Size

```bash
# List all files
aws s3 ls s3://rovnic-ai-audio-storage/ --recursive --summarize

# Check bucket size in GB
aws s3 ls s3://rovnic-ai-audio-storage/ --recursive --summarize --human-readable
```

### View S3 Costs

1. Go to: https://console.aws.amazon.com/billing/
2. Click "Billing Dashboard"
3. Look for S3 charges under "Services"

---

## 🚀 NEXT STEPS

### 1. Add AWS Credentials (Required)
```bash
# Update .env locally
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

# Or update Cloud Run
gcloud run services update rovnic-agent-api \
  --region us-east1 \
  --set-env-vars \
    AWS_ACCESS_KEY_ID=your_key,\
    AWS_SECRET_ACCESS_KEY=your_secret
```

### 2. Test S3 Integration
```bash
# Test locally
python src/services/s3_upload.py output/test.mp3

# Verify file uploaded
aws s3 ls s3://rovnic-ai-audio-storage/
```

### 3. Test API with S3
```bash
# Call prediction endpoint
curl https://rovnic-agent-api-472srmnbna-ue.a.run.app/predict

# Check response for audio_url
```

### 4. Monitor S3 Usage
```bash
# Check bucket
aws s3 ls s3://rovnic-ai-audio-storage/ --recursive --summarize
```

---

## 📋 FILES UPDATED

- ✅ `.env.example` - Added AWS variables
- ✅ `src/services/s3_upload.py` - Added test functionality
- ✅ `Dockerfile` - No changes needed
- ✅ `Cloud Run` - Redeployed with Revision 00005-fhp

---

## 🎊 DEPLOYMENT STATUS

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║     AWS ENVIRONMENT SETUP COMPLETE ✅                      ║
║                                                            ║
║  Status: Configured and ready                             ║
║  Revision: 00005-fhp (live on Cloud Run)                  ║
║  AWS Region: us-east-1                                    ║
║  S3 Bucket: rovnic-ai-audio-storage                       ║
║                                                            ║
║  Variables Set:                                            ║
║  ✅ AWS_DEFAULT_REGION=us-east-1                          ║
║  ✅ AWS_S3_BUCKET=rovnic-ai-audio-storage                 ║
║  ⏳ AWS_ACCESS_KEY_ID (needs credentials)                 ║
║  ⏳ AWS_SECRET_ACCESS_KEY (needs credentials)             ║
║                                                            ║
║  Next: Add your AWS credentials                           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## 📞 QUICK REFERENCE

| Task | Command |
|------|---------|
| Create S3 bucket | `aws s3 mb s3://rovnic-ai-audio-storage --region us-east-1` |
| List bucket files | `aws s3 ls s3://rovnic-ai-audio-storage/` |
| Test S3 locally | `python src/services/s3_upload.py output/test.mp3` |
| Update Cloud Run env | `gcloud run services update rovnic-agent-api --region us-east1 --set-env-vars KEY=VALUE` |
| View Cloud Run config | `gcloud run services describe rovnic-agent-api --region us-east1 --format=yaml` |
| Test API endpoint | `curl https://rovnic-agent-api-472srmnbna-ue.a.run.app/predict` |

---

**Last Updated:** October 28, 2025  
**AWS Setup Status:** ✅ READY FOR CREDENTIALS  
**Deployment Revision:** 00005-fhp  
**Next Action:** Add AWS credentials (Access Key ID & Secret)  

🔑 **Your Rovnic Agentic AI is configured for AWS S3 storage!**
