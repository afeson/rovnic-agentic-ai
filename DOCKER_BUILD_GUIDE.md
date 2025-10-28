# 🐳 Docker Build & Deployment Guide - Rovnic Agentic AI

**Status:** Ready to build when Docker is running  
**Image Name:** `rovnic-agent-api`  
**Base Image:** `python:3.11-slim`  
**Ports:** 8000

---

## 🚀 Quick Start

### Prerequisites

```bash
# 1. Install Docker Desktop
# Windows: https://www.docker.com/products/docker-desktop
# macOS: https://www.docker.com/products/docker-desktop
# Linux: https://docs.docker.com/engine/install/

# 2. Verify Docker is running
docker --version
docker ps
```

### Build Command

```bash
cd C:\Users\afeson\rovnic_agentic_ai\rovnic-agentic-ai

# Build the image
docker build -t rovnic-agent-api .

# Expected output:
# Step 1/11 : FROM python:3.11-slim
# Step 2/11 : WORKDIR /app
# ...
# Step 11/11 : CMD ["python", "-m", "uvicorn", "src.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
# Successfully tagged rovnic-agent-api:latest
```

### Run Container

```bash
# Option 1: Basic run
docker run -p 8000:8000 rovnic-agent-api

# Option 2: With environment variables
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key \
  -e ODDS_API_KEY=your-odds-key \
  -e AWS_ACCESS_KEY_ID=your-aws-key \
  -e AWS_SECRET_ACCESS_KEY=your-aws-secret \
  rovnic-agent-api

# Option 3: With volume mount for .env
docker run -p 8000:8000 \
  --env-file .env \
  rovnic-agent-api
```

### Test Container

```bash
# In another terminal, test the running container
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2025-10-28T15:30:00Z"}

# Test prediction endpoint
curl http://localhost:8000/api/nba

# View Swagger docs
# Open browser: http://localhost:8000/docs
```

### Stop Container

```bash
# Find container ID
docker ps

# Stop it
docker stop <container-id>

# Remove it
docker rm <container-id>
```

---

## 📋 Dockerfile Details

The `Dockerfile` in the project contains:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs models

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 PORT=8000 HOST=0.0.0.0 LOG_LEVEL=INFO ENVIRONMENT=production

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

CMD ["python", "-m", "uvicorn", "src.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key Features:**
- ✅ Python 3.11 slim base image
- ✅ System dependencies installed
- ✅ All Python packages cached for faster builds
- ✅ Logs and models directories created
- ✅ Health check enabled
- ✅ PYTHONUNBUFFERED for real-time logs
- ✅ Uvicorn configured for production

---

## 🏗️ Build Steps Explained

```bash
# 1. Build the image
docker build -t rovnic-agent-api .

# Step 1: Pull base image (python:3.11-slim)
# Step 2: Set working directory (/app)
# Step 3: Install system dependencies (gcc)
# Step 4: Copy requirements.txt
# Step 5: Install Python packages
# Step 6: Copy application code
# Step 7: Create necessary directories
# Step 8: Expose port 8000
# Step 9: Set environment variables
# Step 10: Configure health check
# Step 11: Set startup command

# Result: Docker image tagged as rovnic-agent-api:latest
```

---

## 📊 Image Information

**Image Details:**
```
Repository: rovnic-agent-api
Tag: latest
Base: python:3.11-slim
Size: ~500-600 MB (estimated)
Ports: 8000
Environment: production-ready
```

**Build Time:** ~2-3 minutes (first build)  
**Build Time:** ~10-30 seconds (subsequent builds with cache)

---

## 🐳 Docker Compose (Optional)

Create `docker-compose.yml` for easier orchestration:

```yaml
version: '3.8'

services:
  rovnic-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ODDS_API_KEY=${ODDS_API_KEY}
      - FIREBASE_KEY_PATH=${FIREBASE_KEY_PATH}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_S3_BUCKET=${AWS_S3_BUCKET}
      - PORT=8000
      - ENVIRONMENT=production
    volumes:
      - ./logs:/app/logs
      - ./models:/app/models
      - ./firebase-key.json:/app/firebase-key.json:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
```

**Usage:**
```bash
# Start with docker-compose
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔍 Common Docker Commands

```bash
# View all images
docker images

# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View container logs
docker logs <container-id>
docker logs -f <container-id>  # Follow logs

# Execute command in running container
docker exec -it <container-id> bash

# Remove image
docker rmi rovnic-agent-api

# Remove unused images/containers
docker prune

# Tag image for registry
docker tag rovnic-agent-api myregistry/rovnic-agent-api:1.0

# Push to registry
docker push myregistry/rovnic-agent-api:1.0
```

---

## 🌐 Push to Docker Registry

### Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag rovnic-agent-api <your-username>/rovnic-agent-api:latest

# Push
docker push <your-username>/rovnic-agent-api:latest

# Pull from anywhere
docker pull <your-username>/rovnic-agent-api:latest
```

### Google Container Registry (GCR)

```bash
# Configure authentication
gcloud auth configure-docker

# Tag image
docker tag rovnic-agent-api gcr.io/<project-id>/rovnic-agent-api:latest

# Push
docker push gcr.io/<project-id>/rovnic-agent-api:latest
```

### AWS ECR

```bash
# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag rovnic-agent-api <account-id>.dkr.ecr.us-east-1.amazonaws.com/rovnic-agent-api:latest

# Push
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/rovnic-agent-api:latest
```

---

## ☁️ Deploy Container

### Google Cloud Run

```bash
# Using gcloud command
gcloud run deploy rovnic-agent-api \
  --image gcr.io/<project-id>/rovnic-agent-api:latest \
  --region us-east1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --set-env-vars \
    OPENAI_API_KEY=sk-your-key,\
    ODDS_API_KEY=your-odds-key,\
    AWS_ACCESS_KEY_ID=your-aws-key,\
    AWS_SECRET_ACCESS_KEY=your-aws-secret,\
    AWS_S3_BUCKET=rovnic-voice-summaries
```

### AWS ECS

```bash
# Create task definition
aws ecs register-task-definition \
  --family rovnic-agent-api \
  --container-definitions file://task-def.json

# Run task
aws ecs run-task \
  --cluster default \
  --task-definition rovnic-agent-api
```

### Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy service
docker service create \
  --name rovnic-agent-api \
  --publish 8000:8000 \
  --replicas 3 \
  rovnic-agent-api
```

### Kubernetes

```bash
# Create deployment
kubectl create deployment rovnic-agent-api \
  --image=rovnic-agent-api:latest

# Scale
kubectl scale deployment rovnic-agent-api --replicas=3

# Expose
kubectl expose deployment rovnic-agent-api \
  --port=80 \
  --target-port=8000 \
  --type=LoadBalancer
```

---

## 🐛 Troubleshooting

### Issue: Docker daemon not running

**Solution:**
```bash
# Windows/macOS: Start Docker Desktop
# Linux: Start Docker service
sudo systemctl start docker
```

### Issue: Port already in use

**Solution:**
```bash
# Use different port
docker run -p 8001:8000 rovnic-agent-api

# Or find and stop conflicting container
docker ps
docker stop <container-id>
```

### Issue: Out of disk space

**Solution:**
```bash
# Clean up unused images/containers
docker system prune

# Remove all unused data
docker system prune -a
```

### Issue: Build fails

**Solution:**
```bash
# Rebuild without cache
docker build --no-cache -t rovnic-agent-api .

# Check Dockerfile
cat Dockerfile

# Check requirements.txt
cat requirements.txt
```

---

## ✅ Verification Checklist

- [ ] Docker Desktop installed and running
- [ ] `docker --version` shows version
- [ ] `docker ps` shows running containers
- [ ] `.env` file configured (if mounting)
- [ ] `Dockerfile` exists in project root
- [ ] `requirements.txt` or `requirements-minimal.txt` exists
- [ ] All source files present in `src/` directory
- [ ] Build command runs without errors
- [ ] Container starts: `docker run -p 8000:8000 rovnic-agent-api`
- [ ] Health check passes: `curl http://localhost:8000/health`
- [ ] API responds: `curl http://localhost:8000/api/nba`

---

## 📚 Additional Resources

- Docker Documentation: https://docs.docker.com/
- Docker Best Practices: https://docs.docker.com/develop/dev-best-practices/
- Python in Docker: https://docs.docker.com/language/python/
- FastAPI with Docker: https://fastapi.tiangolo.com/deployment/docker/

---

## 🎯 Next Steps

1. **Build the image:**
   ```bash
   docker build -t rovnic-agent-api .
   ```

2. **Run locally:**
   ```bash
   docker run -p 8000:8000 rovnic-agent-api
   ```

3. **Test it:**
   ```bash
   curl http://localhost:8000/health
   ```

4. **Deploy to cloud:**
   ```bash
   # Choose your platform (Cloud Run, ECS, Kubernetes, etc.)
   gcloud run deploy rovnic-agent-api --image rovnic-agent-api
   ```

---

**Created:** October 28, 2025  
**Status:** Ready for Docker build  
**Next:** Run `docker build -t rovnic-agent-api .` when Docker is running
