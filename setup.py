#!/usr/bin/env python3
"""
Setup script for Voice Detector

System Requirements:
- Python 3.8+
- FFmpeg (required for audio processing)
  - macOS: brew install ffmpeg
  - Ubuntu: sudo apt-get install ffmpeg
  - Windows: Download from https://ffmpeg.org/download.html
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="voice-detector",
    version="1.0.0",
    author="João Ricardo Oliveira",
    author_email="jricardooliveira@gmail.com",
    description="A voice activity detection tool for analyzing audio recordings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jricardooliveira/voice-detector",
    py_modules=["voice_detector"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "voice-detector=voice_detector:main",
        ],
    },
    keywords="voice detection, audio analysis, webrtc, vad, call center, quality monitoring",
    project_urls={
        "Bug Reports": "https://github.com/jricardooliveira/voice-detector/issues",
        "Source": "https://github.com/jricardooliveira/voice-detector",
    },
)