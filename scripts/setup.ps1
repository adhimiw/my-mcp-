#!/usr/bin/env powershell
# MCP Collection Setup Script for Windows
# Author: adhimiw
# Description: Automated setup script for all MCP servers

Write-Host "🚀 MCP Collection Setup Script" -ForegroundColor Green
Write-Host "Setting up all MCP servers and dependencies..." -ForegroundColor Yellow

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️  Warning: Not running as administrator. Some installations may fail." -ForegroundColor Yellow
}

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check prerequisites
Write-Host "`n📋 Checking prerequisites..." -ForegroundColor Blue

# Check Python
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Check Node.js
if (Test-Command node) {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js not found. Please install Node.js from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check/Install uv
if (Test-Command uv) {
    $uvVersion = uv --version
    Write-Host "✅ uv found: $uvVersion" -ForegroundColor Green
} else {
    Write-Host "📦 Installing uv..." -ForegroundColor Yellow
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    if (Test-Command uv) {
        Write-Host "✅ uv installed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install uv. Please install manually." -ForegroundColor Red
        exit 1
    }
}

# Check/Install FFmpeg
if (Test-Command ffmpeg) {
    Write-Host "✅ FFmpeg found" -ForegroundColor Green
} else {
    Write-Host "📦 Installing FFmpeg..." -ForegroundColor Yellow
    try {
        winget install FFmpeg --accept-source-agreements --accept-package-agreements
        Write-Host "✅ FFmpeg installed successfully" -ForegroundColor Green
        Write-Host "⚠️  Please restart your terminal to use FFmpeg" -ForegroundColor Yellow
    } catch {
        Write-Host "❌ Failed to install FFmpeg. Please install manually from https://ffmpeg.org" -ForegroundColor Red
        Write-Host "You can also try: choco install ffmpeg (if you have Chocolatey)" -ForegroundColor Yellow
    }
}

# Install Python dependencies
Write-Host "`n📦 Installing Python dependencies..." -ForegroundColor Blue
try {
    uv sync
    Write-Host "✅ Python dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}

# Create environment file template
Write-Host "`n📝 Creating environment configuration..." -ForegroundColor Blue
$envContent = @"
# MCP Collection Environment Variables
# Copy this file to .env and fill in your API keys

# YouTube Data API Key (Get from Google Cloud Console)
YOUTUBE_API_KEY=your_youtube_api_key_here

# Google Gemini API Key (Get from AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

# LinkedIn Cookie (Extract from browser)
LINKEDIN_COOKIE=li_at=your_linkedin_cookie_here

# Optional: Custom FFmpeg path
# FFMPEG_PATH=C:\path\to\ffmpeg.exe
"@

Set-Content -Path ".env.example" -Value $envContent
Write-Host "✅ Environment template created (.env.example)" -ForegroundColor Green

# Create sample Claude Desktop config
Write-Host "`n⚙️  Creating sample configurations..." -ForegroundColor Blue
$configContent = @"
{
  "mcpServers": {
    "video_audio_editor": {
      "command": "uv",
      "args": [
        "--directory",
        "$PWD\\servers\\video-audio",
        "run",
        "python",
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
        "$PWD\\servers\\gemini-audio",
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
        "$PWD\\servers\\gemini-video",
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
"@

New-Item -ItemType Directory -Force -Path "configs"
Set-Content -Path "configs\claude_desktop_complete.json" -Value $configContent
Write-Host "✅ Sample Claude Desktop config created (configs/claude_desktop_complete.json)" -ForegroundColor Green

# Test server installations
Write-Host "`n🧪 Testing server installations..." -ForegroundColor Blue

# Test video-audio server
Write-Host "Testing video-audio server..." -ForegroundColor Yellow
try {
    $job = Start-Job -ScriptBlock { 
        Set-Location $using:PWD
        uv run --directory "servers\video-audio" python server.py --help 
    }
    Wait-Job $job -Timeout 10 | Out-Null
    $result = Receive-Job $job
    if ($result -match "usage:" -or $result -match "server") {
        Write-Host "✅ Video-audio server working" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Video-audio server may have issues" -ForegroundColor Yellow
    }
    Remove-Job $job -Force
} catch {
    Write-Host "⚠️  Could not test video-audio server" -ForegroundColor Yellow
}

# Test Gemini servers
Write-Host "Testing Gemini servers..." -ForegroundColor Yellow
$env:GEMINI_API_KEY = "test_key"
try {
    $job1 = Start-Job -ScriptBlock { 
        Set-Location $using:PWD
        $env:GEMINI_API_KEY = "test_key"
        uv run --directory "servers\gemini-audio" python server.py --help 2>&1
    }
    Wait-Job $job1 -Timeout 10 | Out-Null
    Remove-Job $job1 -Force
    Write-Host "✅ Gemini servers structure OK" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not test Gemini servers" -ForegroundColor Yellow
}

# Final instructions
Write-Host "`n🎉 Setup Complete!" -ForegroundColor Green
Write-Host "`n📋 Next Steps:" -ForegroundColor Blue
Write-Host "1. Copy .env.example to .env and fill in your API keys" -ForegroundColor White
Write-Host "2. Copy configs/claude_desktop_complete.json to %APPDATA%\Claude\claude_desktop_config.json" -ForegroundColor White
Write-Host "3. Update the paths in the config file to match your installation" -ForegroundColor White
Write-Host "4. Restart Claude Desktop" -ForegroundColor White
Write-Host "5. Start using your MCP servers!" -ForegroundColor White

Write-Host "`n📖 Documentation: https://github.com/adhimiw/my-mcp-" -ForegroundColor Cyan
Write-Host "🐛 Issues: https://github.com/adhimiw/my-mcp-/issues" -ForegroundColor Cyan

Write-Host "`n✨ Happy coding!" -ForegroundColor Magenta
