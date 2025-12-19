import yt_dlp
from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
from typing import List, Optional
import os
from urllib.parse import quote

router = APIRouter()

class VideoFormat(BaseModel):
    format_id: str
    ext: str
    resolution: str
    filesize: Optional[int] = None
    url: Optional[str] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

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
        # Impersonate iOS client to avoid "Sign in" errors
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'web'],
                    'player_skip': ['webpage', 'configs', 'js'], 
                }
            },
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        }
        
        try:
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
                        acodec=f.get('acodec'),
                        width=f.get('width'),
                        height=f.get('height')
                    ))

                return VideoInfo(
                    id=info.get('id'),
                    title=info.get('title'),
                    thumbnail=f"/api/proxy_image?url={quote(info.get('thumbnail'))}" if info.get('thumbnail') else None,
                    duration=info.get('duration'),
                    formats=formats,
                    original_url=url
                )
        except yt_dlp.utils.DownloadError as e:
            error_str = str(e)
            if "Sign in to confirm your age" in error_str:
                raise HTTPException(status_code=403, detail="This video is age-restricted and cannot be downloaded via this tool.")
            elif "Private video" in error_str:
                raise HTTPException(status_code=403, detail="This is a private video and cannot be accessed.")
            elif "Sign in" in error_str:
                 raise HTTPException(status_code=403, detail="This video requires a login/account to view.")
            else:
                raise HTTPException(status_code=400, detail=f"Download Error: {error_str}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/download")
async def get_download_url(url: str, format_id: str):
        # Impersonate iOS client
        ydl_opts = {
            'quiet': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'web'],
                    'player_skip': ['webpage', 'configs', 'js'], 
                }
            },
           'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                found_format = next((f for f in info['formats'] if f['format_id'] == format_id), None)
                
                if not found_format:
                     raise HTTPException(status_code=404, detail="Format not found")
                
                download_url = found_format.get('url')
                if not download_url:
                    raise HTTPException(status_code=404, detail="Download URL not found")

                # Stream the file content
                def iterfile():
                    with requests.get(download_url, stream=True) as r:
                        r.raise_for_status()
                        for chunk in r.iter_content(chunk_size=8192):
                            yield chunk
                
                # Try to guess filename
                ext = found_format.get('ext', 'mp4')
                title = info.get('title', 'video')
                # Sanitize filename (basic)
                filename = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                filename = f"{filename}.{ext}" if filename else f"video.{ext}"

                return StreamingResponse(
                    iterfile(), 
                    media_type="application/octet-stream",
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'}
                )
        except yt_dlp.utils.DownloadError as e:
             error_str = str(e)
             if "Sign in to confirm your age" in error_str:
                 raise HTTPException(status_code=403, detail="This video is age-restricted and cannot be downloaded.")
             elif "Private video" in error_str:
                 raise HTTPException(status_code=403, detail="This is a private video.")
             elif "Sign in" in error_str:
                  raise HTTPException(status_code=403, detail="This video requires a login to view.")
             else:
                 raise HTTPException(status_code=400, detail=f"Download Error: {error_str}")

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/proxy_image")
async def proxy_image(url: str):
    try:
        # We might need headers to mimic a browser so IG doesn't block us
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, stream=True)
        if resp.status_code != 200:
             raise HTTPException(status_code=404, detail="Image not found")
        
        return Response(content=resp.content, media_type=resp.headers.get("Content-Type", "image/jpeg"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
