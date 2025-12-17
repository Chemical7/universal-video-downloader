import yt_dlp
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import os

router = APIRouter()

class VideoFormat(BaseModel):
    format_id: str
    ext: str
    resolution: str
    filesize: Optional[int] = None
    url: Optional[str] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None

class VideoInfo(BaseModel):
    id: str
    title: str
    thumbnail: str
    duration: Optional[float]
    formats: List[VideoFormat]
    original_url: str

@router.get("/info", response_model=VideoInfo)
async def get_video_info(url: str):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False, # We need full info
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Basic parsing of formats
            formats = []
            for f in info.get('formats', []):
                # Filter for useful formats (video+audio, or high quality video)
                # This logic can be refined
                if f.get('protocol') == 'm3u8_native': continue # Skip HLS mostly for direct downloads if possible
                
                formats.append(VideoFormat(
                    format_id=f.get('format_id'),
                    ext=f.get('ext'),
                    resolution=f.get('resolution') or 'audio only',
                    filesize=f.get('filesize'),
                    url=f.get('url'),
                    vcodec=f.get('vcodec'),
                    acodec=f.get('acodec')
                ))

            return VideoInfo(
                id=info.get('id'),
                title=info.get('title'),
                thumbnail=info.get('thumbnail'),
                duration=info.get('duration'),
                formats=formats,
                original_url=url
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/download")
async def get_download_url(url: str, format_id: str):
    """
    For now, return the direct URL if available. 
    In the future/for some sites, we might need to proxy the stream 
    or download-and-serve if the URL is signed/expiring.
    """
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            found_format = next((f for f in info['formats'] if f['format_id'] == format_id), None)
            
            if not found_format:
                 raise HTTPException(status_code=404, detail="Format not found")
            
            return {"direct_url": found_format.get('url')}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
