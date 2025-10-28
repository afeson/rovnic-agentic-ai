# 🐳 Docker Build Instructions - Rovnic Agentic AI

**Date:** October 28, 2025  
**Status:** Ready to build - Docker daemon needs to be running  
**Docker Version:** 28.4.0 (installed ✅)  
**Image Name:** `rovnic-agent-api`  

---

## ⚠️ Current Status

**Docker CLI:** ✅ Installed (version 28.4.0)  
**Docker Daemon:** ⚠️ Not running (Docker Desktop needed)

---

## 🚀 To Build the Docker Image

### Step 1: Start Docker Desktop

**Windows:**
- Open the Windows Start Menu
- Search for "Docker Desktop"
- Click to launch
- Wait for the Docker icon to appear in system tray with green checkmark
- Takes ~30-60 seconds to start

**macOS:**
- Open Applications folder
- Double-click "Docker.app"
- Wait for whale icon in menu bar to settle
- Takes ~30-60 seconds to start

**Linux:**
```bash
sudo systemctl start docker
```

### Step 2: Verify Docker is Running

```bash
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
(empty list if no containers running)
```

**If it shows an error:** Docker daemon is still not running. Wait a bit longer.

### Step 3: Build the Image

```bash
cd C:\Users\afeson\rovnic_agentic_ai\rovnic-agentic-ai

docker build -t rovnic-agent-api .
```

**Expected output:**
```
[+] Building 45.2s (11/11) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [1/11] FROM python:3.11-slim
 => [2/11] WORKDIR /app
 => [3/11] RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
 => [4/11] COPY requirements.txt .
 => [5/11] RUN pip install --no-cache-dir -r requirements.txt
 => [6/11] COPY . .
 => [7/11] RUN mkdir -p logs models
 => [8/11] EXPOSE 8000
 => [9/11] ENV PYTHONUNBUFFERED=1 PORT=8000 HOST=0.0.0.0 LOG_LEVEL=INFO ENVIRONMENT=production
 => [10/11] HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1
 => [11/11] CMD ["python", "-m", "uvicorn", "src.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
 => exporting to image
 => => naming to docker.io/library/rovnic-agent-api:latest

Successfully tagged rovnic-agent-api:latest
```

**Build time:** ~2-3 minutes (first time)

### Step 4: Verify Build Success

```bash
docker images | grep rovnic-agent-api
```

**Expected output:**
```
REPOSITORY           TAG       IMAGE ID      CREATED         SIZE
rovnic-agent-api     latest    abc123def     2 minutes ago    580MB
```

---

## ▶️ Run the Container

```bash
# Basic run
docker run -p 8000:8000 rovnic-agent-api

# With environment variables
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key \
  -e ODDS_API_KEY=your-odds-key \
  rovnic-agent-api

# With .env file
docker run -p 8000:8000 \
  --env-file .env \
  rovnic-agent-api

# In background
docker run -d -p 8000:8000 \
  --name rovnic-agent \
  rovnic-agent-api
```

**Expected output:**
```
[+] Running 1/1
 ⠿ Container abc123def456  Started                                    0.5s

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

## 🧪 Test the Container

**In a new terminal:**

```bash
# Health check
curl http://localhost:8000/health

# Expected: {"status":"healthy","timestamp":"2025-10-28T15:30:00Z"}

# Test prediction endpoint
curl http://localhost:8000/api/nba

# View Swagger docs
# Open in browser: http://localhost:8000/docs
```

---

## 🛑 Stop the Container

```bash
# Find container ID
docker ps

# Stop it
docker stop <container-id>

# Remove it
docker rm <container-id>
```

---

## 📚 Complete Docker Build Guide

For comprehensive Docker documentation including:
- Docker Compose setup
- Pushing to registries (Docker Hub, GCR, ECR)
- Cloud deployments (Cloud Run, ECS, Kubernetes)
- Troubleshooting

See: **DOCKER_BUILD_GUIDE.md**

---

## ✅ Checklist

Before building:
- [ ] Docker Desktop installed
- [ ] Docker Desktop running (green indicator)
- [ ] `docker ps` works without errors
- [ ] `.env` file configured (optional)
- [ ] Dockerfile exists in project root
- [ ] requirements.txt/requirements-minimal.txt exists

After building:
- [ ] `docker images` shows rovnic-agent-api
- [ ] `docker run -p 8000:8000 rovnic-agent-api` starts without errors
- [ ] `curl http://localhost:8000/health` returns 200
- [ ] `http://localhost:8000/docs` loads in browser

---

## 🎯 Quick Summary

```bash
# 1. Start Docker Desktop (Windows/Mac) or systemctl (Linux)

# 2. Build the image
docker build -t rovnic-agent-api .

# 3. Run the container
docker run -p 8000:8000 rovnic-agent-api

# 4. Test it
curl http://localhost:8000/health

# 5. Deploy to cloud
docker push <registry>/rovnic-agent-api:latest
```

---

**Status:** Ready to build! Start Docker Desktop and run:
```bash
docker build -t rovnic-agent-api .
```
