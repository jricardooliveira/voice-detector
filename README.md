# Voice Detector 🎵

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/docker%20hub-jricardooliveira%2Fvoice--detector-blue)](https://hub.docker.com/r/jricardooliveira/voice-detector)

A powerful voice activity detection tool for analyzing audio recordings using Google's WebRTC VAD. Perfect for call center quality monitoring, compliance checking, and automated audio quality assurance.

## System Requirements

### For Docker Usage (Recommended)
- Docker installed on your system
- No additional dependencies required

### For Local Installation
- **Python 3.8+**
- **FFmpeg** (required for audio processing)
- **webrtcvad** Python package
- **setuptools** Python package

## Features

- 🎯 **Accurate Voice Detection** - Uses Google's WebRTC VAD algorithm
- 📁 **Batch Processing** - Analyze entire directories of audio files
- 🐳 **Docker Ready** - Self-contained container with all dependencies
- 📊 **Multiple Output Formats** - Human-readable and JSON output
- ⚙️ **Configurable** - Adjustable thresholds and sensitivity levels
- 🔧 **Easy Integration** - Exit codes for automation and CI/CD

## Installation

### Docker (Recommended)

#### Option 1: Pull from Docker Hub (Easiest)
```bash
# Pull the pre-built image from Docker Hub
docker pull jricardooliveira/voice-detector:latest

# Run directly
docker run --rm -v /path/to/audio:/audio jricardooliveira/voice-detector:latest
```

#### Option 2: Build from source
```bash
# Clone the repository
git clone https://github.com/jricardooliveira/voice-detector.git
cd voice-detector

# Build the Docker image
docker build -t voice-detect .
```

### Local Installation

#### Prerequisites
**FFmpeg is required** for audio processing. Install it first:

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract and add to your PATH
3. Or use chocolatey: `choco install ffmpeg`

**CentOS/RHEL:**
```bash
sudo yum install epel-release
sudo yum install ffmpeg
```

#### Python Installation
```bash
# Clone the repository
git clone https://github.com/jricardooliveira/voice-detector.git
cd voice-detector

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python voice_detector.py --help
```

## Quick Start

### Option 1: Docker Hub (Easiest)
```bash
# Pull and run in one command
docker run --rm -v "/path/to/your/audio/folder":/audio jricardooliveira/voice-detector:latest

# With JSON output
docker run --rm -v "/path/to/your/audio/folder":/audio jricardooliveira/voice-detector:latest --json

# With custom threshold
docker run --rm -v "/path/to/your/audio/folder":/audio jricardooliveira/voice-detector:latest --threshold 0.05
```

### Option 2: Use the helper script (Local build)
```bash
# Make the script executable (first time only)
chmod +x run_voice_detector.sh

# Basic usage
./run_voice_detector.sh "/path/to/your/audio/folder"

# With JSON output
./run_voice_detector.sh "/path/to/your/audio/folder" --json

# With custom threshold
./run_voice_detector.sh "/path/to/your/audio/folder" --threshold 0.05
```

### Option 3: Direct Docker commands
```bash
# Build the container (first time only)
docker build -t voice-detect .

# Basic usage - process all audio files in a directory
docker run --rm -v /path/to/your/audio/folder:/audio voice-detect

# With JSON output
docker run --rm -v /path/to/your/audio/folder:/audio voice-detect --json

# With custom threshold (5% instead of default 10%)
docker run --rm -v /path/to/your/audio/folder:/audio voice-detect --threshold 0.05

# More aggressive voice detection
docker run --rm -v /path/to/your/audio/folder:/audio voice-detect --vad-mode 3
```

## Examples

### Process your "Audios Desktop" folder
```bash
docker run --rm -v "/Users/joaooliveira/dev/python/voicedetect/Audios Desktop":/audio voice-detect
```

### Process with detailed JSON output
```bash
docker run --rm -v "/Users/joaooliveira/dev/python/voicedetect/Audios Desktop":/audio voice-detect --json
```

## Command Line Options

- `--threshold FLOAT`: Minimum voice activity ratio (default: 0.10 = 10%)
- `--frame-ms INT`: Frame duration in milliseconds (10/20/30; default: 30)
- `--vad-mode INT`: VAD aggressiveness (0-3, where 0 is least aggressive, 3 is most aggressive)
- `--json`: Output results in JSON format

## Supported Audio Formats

- MP3
- WAV
- M4A
- AAC
- FLAC
- OGG

## Output

The tool will:
1. Process all audio files in the mounted directory
2. Show progress for each file
3. Report which files have insufficient voice activity
4. Provide a summary with total counts
5. Exit with code 0 (all files have voice) or 2 (some files are silent)

## Exit Codes

- `0`: All files have sufficient voice activity
- `2`: One or more files have insufficient voice activity
- `3`: Processing error

## What it detects

The tool analyzes audio files to identify:
- **Silent recordings** - Files with no or very little voice activity
- **Poor quality calls** - Files where one or both parties have insufficient voice activity
- **Technical issues** - Files that may indicate dropped calls or audio problems

Perfect for call center quality monitoring, compliance checking, and automated audio quality assurance.

## Sharing the Container

### Save the container to a file
```bash
docker save voice-detect > voice-detect.tar
```

### Load the container on another machine
```bash
docker load < voice-detect.tar
```

### Push to a registry (optional)
```bash
# Tag for your registry
docker tag voice-detect your-registry.com/voice-detect:latest

# Push to registry
docker push your-registry.com/voice-detect:latest

# Others can pull it with:
docker pull your-registry.com/voice-detect:latest
```

## File Structure

```
voicedetect/
├── voice_detector.py      # Main voice detection script
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
├── .dockerignore         # Files to ignore when building
├── run_voice_detector.sh # Helper script for easy usage
├── setup.py              # Python package setup
├── LICENSE               # MIT License
├── CONTRIBUTING.md       # Contribution guidelines
└── CHANGELOG.md          # Version history
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**"FFmpeg not found" error:**
- Make sure FFmpeg is installed and in your PATH
- Test with: `ffmpeg -version`
- On Windows, ensure FFmpeg is added to your system PATH

**"webrtcvad module not found" error:**
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**"No audio files found" message:**
- Check that your audio directory contains supported formats (MP3, WAV, M4A, AAC, FLAC, OGG)
- Ensure the directory path is correct and accessible

**Docker permission issues:**
- On Linux/macOS, you might need to add your user to the docker group
- Try running with `sudo` if necessary

## Support

- 📖 **Documentation**: Check this README and [CONTRIBUTING.md](CONTRIBUTING.md)
- 🐛 **Bug Reports**: [Open an issue](https://github.com/jricardooliveira/voice-detector/issues)
- 💡 **Feature Requests**: [Open an issue](https://github.com/jricardooliveira/voice-detector/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/jricardooliveira/voice-detector/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google WebRTC](https://webrtc.org/) for the VAD algorithm
- [FFmpeg](https://ffmpeg.org/) for audio processing capabilities
