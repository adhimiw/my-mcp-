# 🚀 Quick Start Guide - MCP Collection

Get up and running with all 6 MCP servers in under 5 minutes!

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Python 3.8+** installed
- [ ] **Node.js 16+** installed  
- [ ] **Git** installed
- [ ] **Claude Desktop** installed

## ⚡ One-Command Setup

### Windows
```powershell
# Clone and setup everything automatically
git clone https://github.com/adhimiw/my-mcp-.git
cd my-mcp-
.\scripts\setup.ps1
```

### Linux/Mac
```bash
# Clone and setup everything automatically
git clone https://github.com/adhimiw/my-mcp-.git
cd my-mcp-
./scripts/setup.sh
```

## 🔑 Get Your API Keys

While the setup runs, get your API keys:

### 1. YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **YouTube Data API v3**
4. Create credentials → API Key
5. Copy your API key

### 2. Google Gemini API Key
1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click **Get API Key**
3. Create new key or use existing
4. Copy your API key

### 3. LinkedIn Cookie
1. Open LinkedIn in Chrome
2. Press **F12** → **Application** → **Cookies** → `linkedin.com`
3. Find cookie named `li_at`
4. Copy the **Value** (starts with `AQED...`)

## ⚙️ Configure Your Environment

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file with your API keys:**
   ```bash
   YOUTUBE_API_KEY=your_youtube_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   LINKEDIN_COOKIE=li_at=your_linkedin_cookie_here
   ```

## 🎯 Setup Claude Desktop

1. **Copy configuration:**
   ```bash
   # Windows
   copy configs\claude_desktop_complete.json %APPDATA%\Claude\claude_desktop_config.json
   
   # Mac/Linux
   cp configs/claude_desktop_complete.json ~/.config/claude/claude_desktop_config.json
   ```

2. **Update paths in the config file** to match your installation

3. **Restart Claude Desktop**

## ✅ Verify Everything Works

Test each server:

```bash
# Test video-audio server
"Convert a sample MP4 file to MOV format"

# Test YouTube integration
"Search for Python tutorials on YouTube"

# Test LinkedIn automation
"Analyze this LinkedIn profile: https://linkedin.com/in/example"

# Test Canva integration
"Create a social media post design"

# Test audio AI
"Transcribe speech from this audio file"

# Test video AI
"Analyze the content of this video file"
```

## 🎉 You're Ready!

Your AI assistant now has access to:

- 🎬 **Professional video/audio editing**
- 📺 **YouTube data and management** 
- 💼 **LinkedIn automation and research**
- 🎨 **Canva design creation**
- 🎧 **Advanced audio understanding**
- 🎥 **Comprehensive video analysis**

## 🆘 Need Help?

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/adhimiw/my-mcp-/issues)
- 💬 [Ask Questions](https://github.com/adhimiw/my-mcp-/discussions)

## 💡 Pro Tips

1. **Start with small files** to test video/audio processing
2. **YouTube API has quotas** - monitor your usage
3. **LinkedIn cookies expire** every ~30 days
4. **Gemini API is free** for moderate usage
5. **Use absolute paths** in configurations for reliability

---

**Happy coding! 🚀**
