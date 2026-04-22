from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import uvicorn

app = FastAPI()

# Eklentinin erişebilmesi için izinler (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/analyze")
def analyze_user(username: str):
    # Kullanıcı adını temizle
    username = username.replace('@', '').strip()
    url = f"https://www.tiktok.com/@{username}"
    
    print(f"📡 Veri çekiliyor: {username}...")

    # yt-dlp Ayarları
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True, # Video indirme, sadece bilgi al
        'playlistend': 30,    # Son 30 video
        'ignoreerrors': True, 
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # TikTok'tan veriyi çek
            info = ydl.extract_info(url, download=False)
            
            videos = []
            if 'entries' in info:
                for entry in info['entries']:
                    if not entry: continue
                    
                    # --- RESİM DÜZELTME KISMI ---
                    # Önce standart resmi almayı dene
                    cover_url = entry.get("thumbnail")
                    
                    # Eğer standart resim yoksa, resim listesinden en kalitelisini seç
                    if not cover_url and entry.get("thumbnails"):
                        # Listenin sonuncusu genelde en yüksek kalitedir
                        cover_url = entry.get("thumbnails")[-1].get("url")
                    # ---------------------------

                    videos.append({
                        "id": entry.get("id"),
                        "title": entry.get("title") or entry.get("description", "Başlıksız"),
                        "views": entry.get("view_count", 0),
                        "likes": entry.get("like_count", 0),
                        "comments": entry.get("comment_count", 0),
                        "shares": entry.get("repost_count", 0),
                        "cover": cover_url,  # Düzelttiğimiz resmi kullanıyoruz
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
        print(f"Hata: {str(e)}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Sunucuyu başlat
    uvicorn.run(app, host="0.0.0.0", port=8000)
