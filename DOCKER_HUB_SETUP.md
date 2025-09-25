# Docker Hub Setup Guide

## 🐳 Your Docker Image is Now Live on Docker Hub!

**Docker Hub Repository**: https://hub.docker.com/r/jricardooliveira/voice-detector

## What's Available

✅ **Two Tags Published**:
- `jricardooliveira/voice-detector:latest` - Latest version
- `jricardooliveira/voice-detector:1.0.0` - Version 1.0.0

## How Users Can Use Your Image

### Quick Start (No Installation Required)
```bash
# Pull and run in one command
docker run --rm -v "/path/to/audio/folder":/audio jricardooliveira/voice-detector:latest

# With JSON output
docker run --rm -v "/path/to/audio/folder":/audio jricardooliveira/voice-detector:latest --json

# With custom threshold
docker run --rm -v "/path/to/audio/folder":/audio jricardooliveira/voice-detector:latest --threshold 0.05
```

### Pull First, Then Run
```bash
# Pull the image
docker pull jricardooliveira/voice-detector:latest

# Run with your audio files
docker run --rm -v "/path/to/audio":/audio jricardooliveira/voice-detector:latest
```

## Docker Hub Repository Management

### 1. Repository Settings
Go to https://hub.docker.com/r/jricardooliveira/voice-detector and:

1. **Add Description**:
   ```
   A voice activity detection tool for analyzing audio recordings using Google's WebRTC VAD. 
   Perfect for call center quality monitoring, compliance checking, and automated audio quality assurance.
   ```

2. **Add Full Description**:
   ```markdown
   # Voice Detector
   
   A powerful voice activity detection tool for analyzing audio recordings using Google's WebRTC VAD.
   
   ## Features
   - Accurate voice detection using Google's WebRTC VAD algorithm
   - Batch processing of audio directories
   - Support for multiple audio formats (MP3, WAV, M4A, AAC, FLAC, OGG)
   - Configurable thresholds and sensitivity levels
   - JSON and human-readable output formats
   - Docker containerization with all dependencies
   
   ## Quick Start
   ```bash
   docker run --rm -v "/path/to/audio":/audio jricardooliveira/voice-detector:latest
   ```
   
   ## Usage
   ```bash
   # Basic usage
   docker run --rm -v "/path/to/audio":/audio jricardooliveira/voice-detector:latest
   
   # With JSON output
   docker run --rm -v "/path/to/audio":/audio jricardooliveira/voice-detector:latest --json
   
   # With custom threshold
   docker run --rm -v "/path/to/audio":/audio jricardooliveira/voice-detector:latest --threshold 0.05
   ```
   
   ## GitHub Repository
   https://github.com/jricardooliveira/voice-detector
   ```

3. **Add Tags/Keywords**:
   - `voice-detection`
   - `audio-analysis`
   - `webrtc`
   - `vad`
   - `call-center`
   - `quality-monitoring`
   - `python`
   - `ffmpeg`

### 2. Repository Visibility
- Make sure it's **Public** so anyone can pull it
- Enable **Automated Builds** if you want to link it to GitHub

### 3. Automated Builds (Optional)
To automatically build new images when you push to GitHub:

1. Go to **Builds** tab
2. Click **Configure Automated Builds**
3. Connect your GitHub repository
4. Set up build rules:
   - **Source Type**: Branch
   - **Source**: `main`
   - **Docker Tag**: `latest`
   - **Dockerfile Location**: `/Dockerfile`

## Updating Your Image

### Manual Update
```bash
# Rebuild the image
docker build -t voice-detect .

# Tag for Docker Hub
docker tag voice-detect:latest jricardooliveira/voice-detector:latest
docker tag voice-detect:latest jricardooliveira/voice-detector:1.0.1

# Push updates
docker push jricardooliveira/voice-detector:latest
docker push jricardooliveira/voice-detector:1.0.1
```

### Automated Update (Recommended)
Set up automated builds in Docker Hub to automatically build new images when you push to GitHub.

## Usage Statistics

Docker Hub will show you:
- **Pull count** - How many times your image has been downloaded
- **Star count** - How many users have starred your repository
- **Download statistics** - Geographic distribution of downloads

## Sharing Your Image

### Direct Link
Share this link: https://hub.docker.com/r/jricardooliveira/voice-detector

### One-liner for Users
```bash
docker run --rm -v "/path/to/audio":/audio jricardooliveira/voice-detector:latest
```

### In Documentation
```markdown
## Docker Usage

Pull and run the voice detector:

```bash
docker run --rm -v "/path/to/audio":/audio jricardooliveira/voice-detector:latest
```

## Benefits of Docker Hub

✅ **Easy Distribution** - Users can pull with one command  
✅ **No Build Required** - Pre-built image ready to use  
✅ **Version Control** - Multiple tags for different versions  
✅ **Global Access** - Available worldwide via Docker Hub  
✅ **Statistics** - Track usage and popularity  
✅ **Professional** - Standard way to distribute Docker images  

Your voice detector is now easily accessible to anyone with Docker installed! 🚀
