# 🎬 Video/Audio Editor MCP Server

Professional video and audio editing capabilities using FFmpeg integration for AI assistants.

## ✨ Features

### Core Video Operations
- **Format Conversion**: Convert between video formats (MP4, MOV, AVI, MKV, WebM, etc.)
- **Resolution Control**: Change video resolution with quality preservation
- **Codec Management**: Switch between video codecs (H.264, H.265, VP9, etc.)
- **Quality Control**: Adjust video bitrate and frame rates
- **Aspect Ratio**: Modify aspect ratios with padding or cropping

### Audio Processing
- **Audio Extraction**: Extract audio tracks from video files
- **Format Conversion**: Convert between audio formats (MP3, WAV, AAC, FLAC, etc.)
- **Quality Adjustment**: Control audio bitrate and sample rates
- **Channel Management**: Convert between mono and stereo

### Creative Tools
- **Video Trimming**: Cut video segments with precise timing
- **Text Overlays**: Add dynamic text with custom styling and timing
- **Image Overlays**: Insert watermarks and logos
- **Subtitles**: Burn subtitles with custom styling
- **Speed Control**: Create slow-motion or time-lapse effects

### Advanced Editing
- **Video Concatenation**: Join multiple videos with optional transitions
- **B-roll Integration**: Insert B-roll footage with smooth transitions
- **Transitions**: Apply fade in/out effects and crossfades
- **Silence Removal**: Automatically remove silent segments

## 🛠️ Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `extract_audio_from_video` | Extract audio tracks from video files | video_path, output_format |
| `trim_video` | Cut video segments with precise timing | video_path, start_time, end_time |
| `convert_video_format` | Convert between video formats | input_path, output_format |
| `convert_video_properties` | Comprehensive video property conversion | video_path, resolution, codec, bitrate |
| `change_aspect_ratio` | Adjust video aspect ratios | video_path, aspect_ratio, method |
| `set_video_resolution` | Change video resolution | video_path, width, height |
| `set_video_codec` | Switch video codecs | video_path, codec |
| `set_video_bitrate` | Adjust video quality and file size | video_path, bitrate |
| `set_video_frame_rate` | Change playback frame rates | video_path, fps |
| `convert_audio_format` | Convert between audio formats | audio_path, output_format |
| `convert_audio_properties` | Comprehensive audio conversion | audio_path, bitrate, sample_rate |
| `add_subtitles` | Burn subtitles with custom styling | video_path, subtitle_file |
| `add_text_overlay` | Add dynamic text overlays | video_path, text, position, timing |
| `add_image_overlay` | Insert watermarks and logos | video_path, image_path, position |
| `concatenate_videos` | Join multiple videos | video_list, transitions |
| `change_video_speed` | Create speed effects | video_path, speed_factor |
| `remove_silence` | Remove silent segments | audio_path, threshold |

## 📋 Prerequisites

- **FFmpeg** - [Download FFmpeg](https://ffmpeg.org/download.html)
- **Python 3.8+**
- **uv** package manager

## 🚀 Installation

### Using the setup script (Recommended)
```bash
# From the main repository
./scripts/setup.ps1  # Windows
./scripts/setup.sh   # Linux/Mac
```

### Manual Installation
```bash
# Navigate to server directory
cd servers/video-audio

# Install dependencies
uv sync

# Verify FFmpeg installation
ffmpeg -version
```

## ⚙️ Configuration

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "video_audio_editor": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/my-mcp-/servers/video-audio",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

## 📊 Usage Examples

### Video Format Conversion
```bash
"Convert this MP4 file to MOV format with high quality settings"
"Change this AVI video to WebM for web use"
```

### Audio Processing
```bash
"Extract the audio from this video as a high-quality MP3 file"
"Convert this WAV file to AAC with 128kbps bitrate"
```

### Video Editing
```bash
"Trim this video from 30 seconds to 2 minutes"
"Add my company logo as a watermark in the bottom right corner"
"Create a slow-motion effect at 0.5x speed"
```

### Creative Overlays
```bash
"Add the text 'CONFIDENTIAL' as a watermark across the video"
"Burn these SRT subtitles into the video with custom styling"
"Join these three video clips with fade transitions"
```

## 🔧 Supported Formats

### Video Formats
- MP4 (recommended for general use)
- MOV (Apple QuickTime)
- AVI (Audio Video Interleave)
- MKV (Matroska Video)
- WebM (Web video)
- FLV (Flash Video)
- WMV (Windows Media Video)
- M4V (iTunes Video)

### Audio Formats
- MP3 (most compatible)
- WAV (uncompressed)
- AAC (high quality, small size)
- FLAC (lossless)
- OGG (open source)
- M4A (Apple audio)

### Subtitle Formats
- SRT (SubRip)
- VTT (WebVTT)
- ASS/SSA (Advanced SubStation Alpha)

## 🎯 Quality Settings

### Video Quality Presets
- **Ultra High**: 4K, 50+ Mbps
- **High**: 1080p, 10-20 Mbps
- **Medium**: 720p, 5-10 Mbps
- **Low**: 480p, 1-5 Mbps
- **Web**: Optimized for streaming

### Audio Quality Presets
- **Lossless**: FLAC, WAV
- **High**: 320 kbps MP3/AAC
- **Standard**: 192 kbps MP3/AAC
- **Compressed**: 128 kbps MP3/AAC

## 🚨 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```bash
   # Windows
   winget install FFmpeg
   
   # macOS
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt install ffmpeg
   ```

2. **Large file processing**
   - Use appropriate quality settings
   - Consider batch processing for multiple files
   - Monitor system resources during processing

3. **Format compatibility**
   - Check supported formats list
   - Use MP4/H.264 for maximum compatibility
   - Test with smaller files first

### Performance Tips

- **Hardware Acceleration**: Use GPU encoding when available
- **Batch Processing**: Process multiple files together
- **Quality vs Speed**: Balance quality settings with processing time
- **Temporary Files**: Ensure sufficient disk space for processing

## 📈 Performance

### Processing Times (approximate)
- **1080p video (1 min)**: 30-120 seconds
- **4K video (1 min)**: 2-10 minutes
- **Audio conversion**: 5-30 seconds
- **Simple overlay**: 1-3x video length

### System Requirements
- **RAM**: 4GB minimum, 8GB+ recommended
- **Storage**: 2-3x source file size free space
- **CPU**: Multi-core processor recommended for faster processing

## 🔗 Related Tools

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Video Editing Guide](../../docs/video-editing-guide.md)
- [Audio Processing Tips](../../docs/audio-processing.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](../../LICENSE) file for details.

---

**Made with ❤️ using FFmpeg and MCP**
