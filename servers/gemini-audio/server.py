#!/usr/bin/env python3
"""
Audio Understanding MCP Server using Google Gemini API
Allows AI assistants to analyze and understand audio files using Gemini's multimodal capabilities.
"""

import asyncio
import json
import logging
import os
import base64
from pathlib import Path
from typing import Any, Dict, List, Optional
import tempfile
import mimetypes

import google.generativeai as genai
from google.generativeai.types import File as GenAIFile
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("Audio Understanding MCP Server")

# Initialize Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is required")
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)

# Supported audio formats
SUPPORTED_AUDIO_FORMATS = {
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.m4a': 'audio/mp4',
    '.aac': 'audio/aac',
    '.ogg': 'audio/ogg',
    '.flac': 'audio/flac',
    '.weba': 'audio/webm'
}

class AudioAnalyzer:
    """Audio analysis using Google Gemini API"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def _validate_audio_file(self, file_path: str) -> str:
        """Validate audio file and return MIME type"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        extension = path.suffix.lower()
        if extension not in SUPPORTED_AUDIO_FORMATS:
            raise ValueError(f"Unsupported audio format: {extension}. Supported formats: {list(SUPPORTED_AUDIO_FORMATS.keys())}")
        
        return SUPPORTED_AUDIO_FORMATS[extension]
    
    async def upload_audio_file(self, file_path: str):
        """Upload audio file to Gemini"""
        mime_type = self._validate_audio_file(file_path)
        
        # Upload the file
        file = genai.upload_file(file_path, mime_type=mime_type)
        logger.info(f"Uploaded audio file: {file.name}")
        
        # Wait for processing
        while file.state.name == "PROCESSING":
            await asyncio.sleep(1)
            file = genai.get_file(file.name)
        
        if file.state.name == "FAILED":
            raise ValueError(f"Audio file processing failed: {file.state}")
        
        return file
    
    async def analyze_audio(self, file_path: str, prompt: str = None) -> Dict[str, Any]:
        """Analyze audio file with optional custom prompt"""
        try:
            # Upload and process the audio file
            uploaded_file = await self.upload_audio_file(file_path)
            
            # Default analysis prompt
            if not prompt:
                prompt = """Analyze this audio file and provide a comprehensive analysis including:
                1. Transcription of any speech
                2. Audio quality assessment
                3. Background sounds or music
                4. Emotional tone or mood
                5. Language detection (if speech is present)
                6. Audio duration and characteristics
                7. Any notable features or content
                
                Provide the analysis in a structured format."""
            
            # Generate content using the audio file
            response = self.model.generate_content([uploaded_file, prompt])
            
            # Clean up the uploaded file
            genai.delete_file(uploaded_file.name)
            
            return {
                "analysis": response.text,
                "file_info": {
                    "name": Path(file_path).name,
                    "size": Path(file_path).stat().st_size,
                    "mime_type": self._validate_audio_file(file_path)
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing audio: {str(e)}")
            raise
    
    async def transcribe_audio(self, file_path: str) -> Dict[str, Any]:
        """Transcribe speech from audio file"""
        prompt = """Please transcribe all speech in this audio file. 
        Provide the transcription with timestamps if possible, and note:
        - Speaker identification if multiple speakers
        - Any unclear or inaudible parts
        - The confidence level of the transcription
        - Language of the speech"""
        
        return await self.analyze_audio(file_path, prompt)
    
    async def identify_music(self, file_path: str) -> Dict[str, Any]:
        """Identify music and audio characteristics"""
        prompt = """Analyze this audio file for musical content:
        - Genre identification
        - Instrument recognition
        - Tempo and rhythm analysis
        - Mood and energy level
        - Audio quality assessment
        - Any vocals or lyrics (transcribe if present)
        - Similar artists or songs (if recognizable)"""
        
        return await self.analyze_audio(file_path, prompt)
    
    async def detect_audio_events(self, file_path: str) -> Dict[str, Any]:
        """Detect and classify audio events"""
        prompt = """Analyze this audio file for various audio events and sounds:
        - Environmental sounds (traffic, nature, crowds, etc.)
        - Actions or activities (footsteps, doors, machinery, etc.)
        - Animal sounds
        - Vehicle sounds
        - Human activities (typing, cooking, sports, etc.)
        - Any other notable audio events
        
        Provide timestamps and confidence levels for each detected event."""
        
        return await self.analyze_audio(file_path, prompt)

# Initialize analyzer
audio_analyzer = AudioAnalyzer()

@mcp.tool()
async def analyze_audio_file(file_path: str, custom_prompt: str = None) -> Dict[str, Any]:
    """
    Analyze an audio file using Google Gemini's multimodal capabilities.
    
    Args:
        file_path: Path to the audio file to analyze
        custom_prompt: Optional custom analysis prompt
    
    Returns:
        Dictionary containing comprehensive audio analysis
    """
    try:
        result = await audio_analyzer.analyze_audio(file_path, custom_prompt)
        return {
            "success": True,
            "analysis": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def transcribe_speech(file_path: str) -> Dict[str, Any]:
    """
    Transcribe speech from an audio file.
    
    Args:
        file_path: Path to the audio file containing speech
    
    Returns:
        Dictionary containing transcription and metadata
    """
    try:
        result = await audio_analyzer.transcribe_audio(file_path)
        return {
            "success": True,
            "transcription": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def identify_music_content(file_path: str) -> Dict[str, Any]:
    """
    Identify and analyze musical content in an audio file.
    
    Args:
        file_path: Path to the audio file containing music
    
    Returns:
        Dictionary containing music analysis and identification
    """
    try:
        result = await audio_analyzer.identify_music(file_path)
        return {
            "success": True,
            "music_analysis": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def detect_audio_events(file_path: str) -> Dict[str, Any]:
    """
    Detect and classify various audio events in an audio file.
    
    Args:
        file_path: Path to the audio file to analyze for events
    
    Returns:
        Dictionary containing detected audio events and classifications
    """
    try:
        result = await audio_analyzer.detect_audio_events(file_path)
        return {
            "success": True,
            "events": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_supported_formats() -> Dict[str, List[str]]:
    """
    Get list of supported audio formats.
    
    Returns:
        Dictionary containing supported audio file extensions and MIME types
    """
    return {
        "supported_extensions": list(SUPPORTED_AUDIO_FORMATS.keys()),
        "supported_mime_types": list(SUPPORTED_AUDIO_FORMATS.values())
    }

@mcp.tool()
async def audio_quality_check(file_path: str) -> Dict[str, Any]:
    """
    Check audio quality and provide technical analysis.
    
    Args:
        file_path: Path to the audio file to check
    
    Returns:
        Dictionary containing audio quality assessment
    """
    prompt = """Analyze the technical quality of this audio file:
    - Audio bitrate and sample rate (if determinable)
    - Dynamic range and compression
    - Noise level and signal-to-noise ratio
    - Clipping or distortion issues
    - Overall audio quality rating (1-10)
    - Recommendations for improvement
    - Suitability for different use cases (podcast, music, speech recognition, etc.)"""
    
    try:
        result = await audio_analyzer.analyze_audio(file_path, prompt)
        return {
            "success": True,
            "quality_analysis": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
