# 🚀 My MCP Collection - Advanced AI Model Context Protocol Servers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

A comprehensive collection of Model Context Protocol (MCP) servers that extend AI assistants with powerful capabilities including video/audio editing, LinkedIn automation, YouTube integration, and advanced multimedia analysis using Google Gemini.

## 🌟 Featured Servers

| Server | Description | Key Features |
|--------|-------------|--------------|
| **🎬 Video/Audio Editor** | Professional video/audio editing with FFmpeg | Format conversion, trimming, overlays, transitions |
| **🎨 Canva Integration** | Design creation and editing | Templates, brand kits, export capabilities |
| **💼 LinkedIn Automation** | LinkedIn profile & job analysis | Profile scraping, job search, company research |
| **📺 YouTube Integration** | YouTube data and video management | Video search, channel analysis, metadata extraction |
| **🎧 Audio Gemini AI** | Advanced audio understanding | Speech transcription, music analysis, sound detection |
| **🎥 Video Gemini AI** | Comprehensive video analysis | Scene extraction, object detection, quality assessment |

## 📦 Quick Start

### Prerequisites
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **uv** (recommended) - [Install uv](https://docs.astral.sh/uv/)
- **FFmpeg** - [Install FFmpeg](https://ffmpeg.org/download.html)

### 🔧 Installation

#### Option 1: Quick Setup Script (Recommended)
```bash
# Clone the repository
git clone https://github.com/adhimiw/my-mcp-.git
cd my-mcp-

# Run the setup script
./scripts/setup.sh  # Linux/Mac
# or
.\scripts\setup.ps1  # Windows
```

#### Option 2: Manual Installation
```bash
# Clone and navigate
git clone https://github.com/adhimiw/my-mcp-.git
cd my-mcp-

# Install dependencies
uv sync

# Install additional requirements
uv add google-generativeai ffmpeg-python
```

## 🎯 Server Configurations

### Complete Configuration (All Servers)
Add this to your Claude Desktop config (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "video_audio_editor": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/my-mcp-/servers/video-audio",
        "run",
        "server.py"
      ]
    },
    "canva": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://mcp.canva.com/mcp"
      ]
    },
    "linkedin": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/stickerdaniel/linkedin-mcp-server",
        "linkedin-mcp-server"
      ],
      "env": {
        "LINKEDIN_COOKIE": "li_at=YOUR_LINKEDIN_COOKIE"
      }
    },
    "youtube": {
      "command": "npx",
      "args": [
        "-y",
        "yt-mcp"
      ],
      "env": {
        "YOUTUBE_API_KEY": "YOUR_YOUTUBE_API_KEY"
      }
    },
    "audio_gemini": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/my-mcp-/servers/gemini-audio",
        "run",
        "python",
        "server.py"
      ],
      "env": {
        "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY"
      }
    },
    "video_gemini": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/my-mcp-/servers/gemini-video",
        "run",
        "python",
        "server.py"
      ],
      "env": {
        "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY"
      }
    }
  }
}
```

## 📚 Individual Server Documentation

### 🎬 Video/Audio Editor Server
Professional video and audio editing capabilities using FFmpeg.

**Key Features:**
- Video format conversion (MP4, MOV, AVI, etc.)
- Audio extraction and processing
- Video trimming and speed adjustment
- Text overlays and watermarks
- Professional transitions and effects

[📖 Full Documentation](./servers/video-audio/README.md)

### 🎨 Canva Integration Server
Direct integration with Canva's design platform.

**Key Features:**
- Design creation and editing
- Template access
- Brand kit integration
- Export in multiple formats

[📖 Full Documentation](./docs/canva-integration.md)

### 💼 LinkedIn Automation Server
Comprehensive LinkedIn automation and data extraction.

**Key Features:**
- Profile scraping and analysis
- Job search automation
- Company research
- Networking insights

[📖 Full Documentation](./docs/linkedin-automation.md)

### 📺 YouTube Integration Server
Complete YouTube data API integration.

**Key Features:**
- Video search and analysis
- Channel information
- Playlist management
- Metadata extraction

[📖 Full Documentation](./docs/youtube-integration.md)

### 🎧 Audio Gemini AI Server
Advanced audio understanding using Google Gemini.

**Key Features:**
- Speech transcription with timestamps
- Music genre and instrument identification
- Audio quality assessment
- Sound event detection

[📖 Full Documentation](./servers/gemini-audio/README.md)

### 🎥 Video Gemini AI Server
Comprehensive video analysis using Google Gemini.

**Key Features:**
- Scene extraction and description
- Object and person identification
- Activity detection
- Content safety analysis

[📖 Full Documentation](./servers/gemini-video/README.md)

## 🔑 API Keys & Configuration

### Required API Keys

1. **YouTube API Key** - [Get from Google Cloud Console](https://console.cloud.google.com/)
2. **Gemini API Key** - [Get from Google AI Studio](https://ai.google.dev/)
3. **LinkedIn Cookie** - Extract from browser (see LinkedIn docs)

### Environment Setup

Create a `.env` file in the root directory:

```bash
# API Keys
YOUTUBE_API_KEY=your_youtube_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
LINKEDIN_COOKIE=li_at=your_linkedin_cookie_here

# Optional: Custom paths
FFMPEG_PATH=/usr/local/bin/ffmpeg
```

## 🛠️ Development

### Project Structure
```
my-mcp-/
├── servers/
│   ├── video-audio/          # Video/Audio editing server
│   ├── gemini-audio/          # Audio AI analysis server
│   └── gemini-video/          # Video AI analysis server
├── scripts/
│   ├── setup.sh              # Linux/Mac setup script
│   ├── setup.ps1             # Windows setup script
│   └── test-servers.py       # Server testing script
├── docs/                     # Detailed documentation
├── examples/                 # Usage examples
├── configs/                  # Sample configurations
└── tests/                    # Unit tests
```

### Running Tests
```bash
# Test all servers
python scripts/test-servers.py

# Test specific server
python scripts/test-servers.py --server video_audio

# Run unit tests
pytest tests/
```

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Usage Examples

### Video Editing
```bash
# Convert video format
"Convert this MP4 file to MOV format with high quality settings"

# Add watermark
"Add my company logo as a watermark to this video in the bottom right corner"

# Extract audio
"Extract the audio from this video as a high-quality MP3 file"
```

### AI Analysis
```bash
# Analyze audio content
"Transcribe this podcast episode and identify the main topics discussed"

# Video scene analysis
"Extract key scenes from this video and provide detailed descriptions"

# Content safety check
"Analyze this video for content appropriateness and platform suitability"
```

### LinkedIn Automation
```bash
# Research profiles
"Analyze this LinkedIn profile and provide insights for networking"

# Job searching
"Find marketing manager jobs in San Francisco and analyze the requirements"
```

## 🚨 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Install FFmpeg: `winget install FFmpeg` (Windows) or `brew install ffmpeg` (Mac)
   - Add to PATH environment variable

2. **Python module errors**
   - Ensure you're using `uv run` for Python commands
   - Install missing dependencies: `uv add [package-name]`

3. **API key issues**
   - Verify API keys are correctly set in environment variables
   - Check API quotas and permissions

4. **MCP connection errors**
   - Restart Claude Desktop after configuration changes
   - Verify JSON configuration syntax

### Getting Help

- 📖 Check the [Troubleshooting Guide](./docs/troubleshooting.md)
- 🐛 [Report Issues](https://github.com/adhimiw/my-mcp-/issues)
- 💬 [Discussions](https://github.com/adhimiw/my-mcp-/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic
- [Google Gemini API](https://ai.google.dev/) for AI capabilities
- [FFmpeg](https://ffmpeg.org/) for multimedia processing
- Community contributors and testers

## 🔮 Roadmap

- [ ] Web interface for server management
- [ ] Docker containerization
- [ ] Additional AI model integrations
- [ ] Real-time streaming capabilities
- [ ] Batch processing features

---

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ by [adhimiw](https://github.com/adhimiw)
