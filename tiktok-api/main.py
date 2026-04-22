"""
TikTok API - FastAPI + yt-dlp
Railway Deployment Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

app = FastAPI(
    title="TikTok Analysis API",
    description="API for analyzing TikTok user profiles and videos",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {
        "success": True,
        "message": "TikTok API is running",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze?username=<username>"
        }
    }


@app.get("/api/analyze")
def analyze_user(username: str):
    """
    Analyze TikTok user and get their recent videos
    
    Args:
        username: TikTok username (with or without @)
    
    Returns:
        JSON with user's video data
    """
    username = username.replace("@", "").strip()
    
    if not username:
        return {
            "success": False,
            "error": "Username is required"
        }
    
    url = f"https://www.tiktok.com/@{username}"

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "playlistend": 30,
        "ignoreerrors": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            videos = []
            if "entries" in info and info["entries"]:
                for entry in info["entries"]:
                    if not entry:
                        continue

                    cover_url = entry.get("thumbnail")
                    if not cover_url and entry.get("thumbnails"):
                        cover_url = entry.get("thumbnails")[-1].get("url")

                    videos.append(
                        {
                            "id": entry.get("id"),
                            "title": entry.get("title") or entry.get("description", "Untitled"),
                            "views": entry.get("view_count", 0),
                            "likes": entry.get("like_count", 0),
                            "comments": entry.get("comment_count", 0),
                            "shares": entry.get("repost_count", 0),
                            "cover": cover_url,
                            "playUrl": entry.get("webpage_url"),
                            "create_time": entry.get("timestamp"),
                        }
                    )

            return {
                "success": True,
                "username": username,
                "video_count": len(videos),
                "data": videos,
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "username": username
        }


# For local development
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
