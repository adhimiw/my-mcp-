#!/usr/bin/env python3
"""
Video Understanding MCP Server using Google Gemini API
Allows AI assistants to analyze and understand video files using Gemini's multimodal capabilities.
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
import time

import google.generativeai as genai
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("Video Understanding MCP Server")

# Initialize Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is required")
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)

# Supported video formats
SUPPORTED_VIDEO_FORMATS = {
    '.mp4': 'video/mp4',
    '.mov': 'video/quicktime',
    '.avi': 'video/x-msvideo',
    '.mkv': 'video/x-matroska',
    '.webm': 'video/webm',
    '.flv': 'video/x-flv',
    '.wmv': 'video/x-ms-wmv',
    '.m4v': 'video/mp4'
}

class VideoAnalyzer:
    """Video analysis using Google Gemini API"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def _validate_video_file(self, file_path: str) -> str:
        """Validate video file and return MIME type"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Video file not found: {file_path}")
        
        extension = path.suffix.lower()
        if extension not in SUPPORTED_VIDEO_FORMATS:
            raise ValueError(f"Unsupported video format: {extension}. Supported formats: {list(SUPPORTED_VIDEO_FORMATS.keys())}")
        
        return SUPPORTED_VIDEO_FORMATS[extension]
    
    async def upload_video_file(self, file_path: str):
        """Upload video file to Gemini"""
        mime_type = self._validate_video_file(file_path)
        
        # Upload the file
        file = genai.upload_file(file_path, mime_type=mime_type)
        logger.info(f"Uploaded video file: {file.name}")
        
        # Wait for processing
        while file.state.name == "PROCESSING":
            logger.info("Video processing... waiting")
            await asyncio.sleep(2)
            file = genai.get_file(file.name)
        
        if file.state.name == "FAILED":
            raise ValueError(f"Video file processing failed: {file.state}")
        
        logger.info(f"Video processing completed: {file.state.name}")
        return file
    
    async def analyze_video(self, file_path: str, prompt: str = None) -> Dict[str, Any]:
        """Analyze video file with optional custom prompt"""
        try:
            # Upload and process the video file
            uploaded_file = await self.upload_video_file(file_path)
            
            # Default analysis prompt
            if not prompt:
                prompt = """Analyze this video comprehensively and provide detailed insights including:
                
                1. **Visual Content Analysis:**
                   - Scene descriptions and key visual elements
                   - Objects, people, and activities identified
                   - Setting and environment description
                   - Color schemes and visual composition
                
                2. **Motion and Action Analysis:**
                   - Camera movements and angles
                   - Subject movements and actions
                   - Scene transitions and cuts
                   - Overall pacing and rhythm
                
                3. **Audio Content (if present):**
                   - Speech transcription and speaker identification
                   - Background music or sound effects
                   - Audio quality and clarity
                   - Emotional tone from audio
                
                4. **Technical Analysis:**
                   - Video quality and resolution assessment
                   - Lighting conditions and quality
                   - Production quality evaluation
                   - Any technical issues noticed
                
                5. **Content Classification:**
                   - Genre or category identification
                   - Target audience assessment
                   - Content themes and messages
                   - Emotional impact and mood
                
                6. **Temporal Analysis:**
                   - Key moments and timestamps
                   - Story structure or progression
                   - Important events chronologically
                
                Please provide the analysis in a well-structured format with clear sections."""
            
            # Generate content using the video file
            response = self.model.generate_content([uploaded_file, prompt])
            
            # Clean up the uploaded file
            genai.delete_file(uploaded_file.name)
            
            return {
                "analysis": response.text,
                "file_info": {
                    "name": Path(file_path).name,
                    "size": Path(file_path).stat().st_size,
                    "mime_type": self._validate_video_file(file_path)
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing video: {str(e)}")
            raise
    
    async def extract_scenes(self, file_path: str) -> Dict[str, Any]:
        """Extract and describe key scenes from video"""
        prompt = """Analyze this video and extract key scenes. For each scene, provide:
        
        - Scene number and approximate timestamp
        - Detailed visual description
        - Key objects, people, and actions
        - Setting and location description
        - Emotional tone or mood of the scene
        - Significance or importance to the overall content
        - Any dialogue or important audio elements
        
        Focus on identifying distinct scenes and major transitions. Provide timestamps where possible."""
        
        return await self.analyze_video(file_path, prompt)
    
    async def transcribe_video_speech(self, file_path: str) -> Dict[str, Any]:
        """Transcribe all speech and dialogue from video"""
        prompt = """Transcribe all speech and dialogue in this video. Provide:
        
        - Complete transcription of all spoken words
        - Speaker identification (if multiple speakers)
        - Timestamps for different segments
        - Tone and emotional delivery notes
        - Any background audio or music descriptions
        - Confidence level of transcription
        - Language identification
        - Non-verbal audio cues (laughter, applause, etc.)
        
        Format the output as a clear transcript with speaker labels and timestamps."""
        
        return await self.analyze_video(file_path, prompt)
    
    async def identify_objects_people(self, file_path: str) -> Dict[str, Any]:
        """Identify and catalog objects, people, and entities in the video"""
        prompt = """Analyze this video to identify and catalog all visible elements:
        
        **People:**
        - Number of people visible
        - Age groups and demographics
        - Clothing and appearance descriptions
        - Actions and behaviors
        - Facial expressions and emotions (if visible)
        
        **Objects:**
        - All significant objects and items
        - Brands or text visible in the video
        - Technology and devices shown
        - Furniture and environment elements
        
        **Locations and Settings:**
        - Indoor/outdoor classification
        - Type of location (office, home, street, etc.)
        - Architectural features
        - Geographic or cultural indicators
        
        **Activities and Events:**
        - Main activities taking place
        - Interactions between people
        - Use of objects and tools
        
        Provide detailed descriptions and timestamps where possible."""
        
        return await self.analyze_video(file_path, prompt)
    
    async def analyze_video_quality(self, file_path: str) -> Dict[str, Any]:
        """Analyze technical video quality aspects"""
        prompt = """Analyze the technical quality of this video and provide assessment on:
        
        **Visual Quality:**
        - Resolution and clarity assessment
        - Color accuracy and saturation
        - Brightness and contrast levels
        - Sharpness and focus quality
        - Any visual artifacts or issues
        
        **Production Quality:**
        - Camera work and stability
        - Framing and composition
        - Lighting quality and consistency
        - Professional production indicators
        
        **Audio Quality:**
        - Audio clarity and volume levels
        - Background noise assessment
        - Audio-video synchronization
        - Overall sound production quality
        
        **Technical Issues:**
        - Compression artifacts
        - Frame rate issues
        - Any glitches or problems
        - File corruption indicators
        
        **Overall Assessment:**
        - Quality rating (1-10 scale)
        - Suitability for different purposes
        - Recommendations for improvement
        - Best use cases for this video quality level"""
        
        return await self.analyze_video(file_path, prompt)
    
    async def detect_actions_activities(self, file_path: str) -> Dict[str, Any]:
        """Detect and classify actions and activities in the video"""
        prompt = """Analyze this video to detect and classify all actions and activities:
        
        **Human Actions:**
        - Physical movements and gestures
        - Facial expressions and emotions
        - Interactions with objects or people
        - Sports or exercise activities
        - Work-related activities
        
        **Environmental Activities:**
        - Weather conditions and changes
        - Traffic and vehicle movements
        - Nature activities (animals, water, etc.)
        - Crowd movements and behaviors
        
        **Event Detection:**
        - Meetings or presentations
        - Entertainment or performance events
        - Educational or instructional content
        - Social gatherings or celebrations
        
        **Temporal Analysis:**
        - Duration of each activity
        - Sequence and order of events
        - Simultaneous activities
        - Activity transitions and changes
        
        Provide timestamps and confidence levels for each detected activity."""
        
        return await self.analyze_video(file_path, prompt)

# Initialize analyzer
video_analyzer = VideoAnalyzer()

@mcp.tool()
async def analyze_video_file(file_path: str, custom_prompt: str = None) -> Dict[str, Any]:
    """
    Analyze a video file using Google Gemini's multimodal video understanding capabilities.
    
    Args:
        file_path: Path to the video file to analyze
        custom_prompt: Optional custom analysis prompt
    
    Returns:
        Dictionary containing comprehensive video analysis
    """
    try:
        result = await video_analyzer.analyze_video(file_path, custom_prompt)
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
async def extract_key_scenes(file_path: str) -> Dict[str, Any]:
    """
    Extract and describe key scenes from a video file.
    
    Args:
        file_path: Path to the video file
    
    Returns:
        Dictionary containing scene analysis and descriptions
    """
    try:
        result = await video_analyzer.extract_scenes(file_path)
        return {
            "success": True,
            "scenes": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def transcribe_video_audio(file_path: str) -> Dict[str, Any]:
    """
    Transcribe all speech and dialogue from a video file.
    
    Args:
        file_path: Path to the video file containing speech
    
    Returns:
        Dictionary containing video transcription and metadata
    """
    try:
        result = await video_analyzer.transcribe_video_speech(file_path)
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
async def identify_video_objects(file_path: str) -> Dict[str, Any]:
    """
    Identify and catalog all objects, people, and entities visible in a video.
    
    Args:
        file_path: Path to the video file to analyze
    
    Returns:
        Dictionary containing identified objects and people
    """
    try:
        result = await video_analyzer.identify_objects_people(file_path)
        return {
            "success": True,
            "identification": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def assess_video_quality(file_path: str) -> Dict[str, Any]:
    """
    Analyze the technical quality aspects of a video file.
    
    Args:
        file_path: Path to the video file to assess
    
    Returns:
        Dictionary containing video quality assessment
    """
    try:
        result = await video_analyzer.analyze_video_quality(file_path)
        return {
            "success": True,
            "quality_assessment": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def detect_video_activities(file_path: str) -> Dict[str, Any]:
    """
    Detect and classify actions and activities occurring in a video.
    
    Args:
        file_path: Path to the video file to analyze
    
    Returns:
        Dictionary containing detected activities and actions
    """
    try:
        result = await video_analyzer.detect_actions_activities(file_path)
        return {
            "success": True,
            "activities": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_video_supported_formats() -> Dict[str, List[str]]:
    """
    Get list of supported video formats for analysis.
    
    Returns:
        Dictionary containing supported video file extensions and MIME types
    """
    return {
        "supported_extensions": list(SUPPORTED_VIDEO_FORMATS.keys()),
        "supported_mime_types": list(SUPPORTED_VIDEO_FORMATS.values())
    }

@mcp.tool()
async def analyze_video_content_safety(file_path: str) -> Dict[str, Any]:
    """
    Analyze video content for safety, appropriateness, and content classification.
    
    Args:
        file_path: Path to the video file to analyze
    
    Returns:
        Dictionary containing content safety analysis
    """
    prompt = """Analyze this video for content safety and appropriateness:
    
    **Content Classification:**
    - Age appropriateness rating
    - Content category (educational, entertainment, etc.)
    - Target audience identification
    
    **Safety Assessment:**
    - Potentially sensitive content identification
    - Violence or aggressive behavior detection
    - Inappropriate language or content
    - Adult content indicators
    
    **Compliance Analysis:**
    - Platform suitability (YouTube, social media, etc.)
    - Educational content assessment
    - Professional content evaluation
    
    **Content Themes:**
    - Main topics and subjects covered
    - Educational value assessment
    - Entertainment value evaluation
    - Information accuracy (if factual content)
    
    Provide recommendations for content usage and distribution."""
    
    try:
        result = await video_analyzer.analyze_video(file_path, prompt)
        return {
            "success": True,
            "content_safety": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
