# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Initial release of Voice Detector
- Voice activity detection using Google's WebRTC VAD
- Support for multiple audio formats (MP3, WAV, M4A, AAC, FLAC, OGG)
- Stereo and mono audio processing
- Configurable voice activity threshold
- JSON output format
- Docker containerization
- Command-line interface with multiple options
- Batch processing of audio files in directories
- Progress tracking and detailed reporting
- Exit codes for automation integration

### Features
- **Audio Processing**: Converts audio to 16-bit PCM mono at 16kHz
- **Voice Detection**: Uses WebRTC VAD with configurable sensitivity (0-3)
- **Channel Analysis**: Supports both mono and stereo recordings
- **Threshold Detection**: Configurable minimum voice activity ratio (default: 10%)
- **Output Formats**: Human-readable and JSON output
- **Docker Support**: Self-contained container with all dependencies
- **Helper Scripts**: Easy-to-use shell script for Docker operations

### Technical Details
- **Dependencies**: webrtcvad, setuptools, ffmpeg
- **Python Version**: 3.8+
- **Platform Support**: Linux, macOS, Windows (with Docker)
- **Audio Formats**: MP3, WAV, M4A, AAC, FLAC, OGG
- **Frame Sizes**: 10ms, 20ms, 30ms (configurable)

### Use Cases
- Call center quality monitoring
- Audio quality assurance
- Compliance checking
- Automated monitoring systems
- CI/CD pipeline integration
