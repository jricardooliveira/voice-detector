FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the voice detection script
COPY voice_detector.py .

# Make the script executable
RUN chmod +x voice_detector.py

# Create a directory for mounting audio files
RUN mkdir -p /audio

# Set the default command
ENTRYPOINT ["python", "voice_detector.py", "/audio"]
