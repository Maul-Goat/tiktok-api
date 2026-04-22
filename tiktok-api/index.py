from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import uvicorn
import os

app = FastAPI(title="TikTok Analysis API", version="1.0.0")

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
        "version": "1.0.0"
    }

@app.get("/api/analyze")
def analyze_user(username: str):
    """Analyze TikTok user and get recent videos"""
    username = username.replace('@', '').strip()
    
    if not username:
        return {"success": False, "error": "Username is required"}
    
    url = f"https://www.tiktok.com/@{username}"
    
    print(f"📡 Fetching data for: {username}...")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'playlistend': 30,
        'ignoreerrors': True, 
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            videos = []
            if 'entries' in info and info['entries']:
                for entry in info['entries']:
                    if not entry:
                        continue
                    
                    cover_url = entry.get("thumbnail")
                    if not cover_url and entry.get("thumbnails"):
                        cover_url = entry.get("thumbnails")[-1].get("url")

                    videos.append({
                        "id": entry.get("id"),
                        "title": entry.get("title") or entry.get("description", "Untitled"),
                        "views": entry.get("view_count", 0),
                        "likes": entry.get("like_count", 0),
                        "comments": entry.get("comment_count", 0),
                        "shares": entry.get("repost_count", 0),
                        "cover": cover_url,
                        "playUrl": entry.get("webpage_url"),
                        "create_time": entry.get("timestamp")
                    })

            return {
                "success": True, 
                "username": username,
                "video_count": len(videos),
                "data": videos
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
