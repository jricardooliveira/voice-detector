#!/bin/bash

# Voice Detection Docker Runner
# Usage: ./run_voice_detector.sh [audio_directory] [options]

# Default values
AUDIO_DIR="${1:-./audio}"
DOCKER_IMAGE="jricardooliveira/voice-detector:latest"
SHIFT_ARGS=1

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if the audio directory exists
if [ ! -d "$AUDIO_DIR" ]; then
    echo "❌ Audio directory '$AUDIO_DIR' does not exist."
    echo "Usage: $0 [audio_directory] [options]"
    echo "Example: $0 '/path/to/audio/folder' --json"
    exit 1
fi

# Get absolute path
AUDIO_DIR=$(cd "$AUDIO_DIR" && pwd)

echo "🎵 Processing audio files in: $AUDIO_DIR"
echo "🐳 Using Docker image: $DOCKER_IMAGE"
echo ""

# Run the Docker container with all remaining arguments
docker run --rm \
    -v "$AUDIO_DIR:/audio" \
    "$DOCKER_IMAGE" \
    "${@:$SHIFT_ARGS+1}"

echo ""
echo "✅ Analysis complete!"
