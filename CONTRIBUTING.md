# Contributing to Voice Detector

Thank you for your interest in contributing to Voice Detector! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker (for containerized development)
- FFmpeg (for audio processing)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jricardooliveira/voice-detector.git
   cd voice-detector
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from https://ffmpeg.org/download.html

## Development Workflow

### Running Tests

```bash
# Run the script locally
python voice_detector.py /path/to/audio/folder

# Test with Docker
docker build -t voice-detect .
docker run --rm -v /path/to/audio:/audio voice-detect
```

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test your changes thoroughly**
5. **Commit with a clear message**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

## Types of Contributions

### Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

### Feature Requests

For new features, please:
- Describe the use case
- Explain why it would be valuable
- Consider backward compatibility

### Code Contributions

We welcome contributions for:
- Bug fixes
- Performance improvements
- New features
- Documentation improvements
- Test coverage

## Docker Development

### Building the Container

```bash
docker build -t voice-detect .
```

### Testing the Container

```bash
# Test with sample audio
docker run --rm -v /path/to/audio:/audio voice-detect

# Test with options
docker run --rm -v /path/to/audio:/audio voice-detect --json --threshold 0.05
```

## Release Process

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create a git tag
4. Build and test Docker image
5. Create GitHub release

## Questions?

Feel free to open an issue for any questions or discussions about contributing.
