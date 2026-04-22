# 🚂 Railway Deployment Guide - TikTok API

## ✅ File Structure (Sudah Benar)

```
tiktok-api/
├── main.py              ← Entry point (WAJIB)
├── requirements.txt     ← Dependencies
├── Procfile            ← Railway start command
├── railway.toml        ← Railway config
├── nixpacks.toml       ← Nixpacks config
├── runtime.txt         ← Python version
└── api/
    └── index.py        ← Legacy (tidak dipakai lagi)
```

## 🚀 Cara Deploy ke Railway

### **Method 1: Deploy dari GitHub (Recommended)**

1. **Push code ke GitHub**
   ```bash
   git add .
   git commit -m "Fix Railway deployment structure"
   git push origin main
   ```

2. **Login Railway**
   - Buka https://railway.app
   - Login dengan GitHub

3. **Create New Project**
   - Click "New Project"
   - Pilih "Deploy from GitHub repo"
   - Authorize Railway
   - Pilih repository kamu

4. **Configure Service**
   - Railway akan auto-detect Python
   - **Root Directory:** 
     - Jika mono-repo: Set ke `/tiktok-api`
     - Jika single repo: Biarkan kosong `/`
   - Railway akan otomatis:
     - Detect `main.py`
     - Install dari `requirements.txt`
     - Run command dari `Procfile`

5. **Generate Domain**
   - Settings → Networking → Generate Domain
   - Catat URL: `https://tiktok-api-production.up.railway.app`

6. **Test Deployment**
   ```bash
   # Health check
   curl https://tiktok-api-production.up.railway.app/
   
   # Test analyze endpoint
   curl "https://tiktok-api-production.up.railway.app/api/analyze?username=kaycee"
   ```

---

### **Method 2: Deploy dari Railway CLI**

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
cd tiktok-api
railway init

# Deploy
railway up

# Generate domain
railway domain
```

---

## 🔧 Troubleshooting

### **Error: "No Python version specified"**

✅ **Sudah fixed** dengan `runtime.txt`

### **Error: "Module not found"**

Check:
- `requirements.txt` ada dan benar
- Railway logs: `railway logs`

### **Error: "Port binding failed"**

✅ **Sudah fixed** - Railway auto-set `$PORT` environment variable

### **Error: "yt-dlp not working"**

Railway sudah include `ffmpeg` di `nixpacks.toml`

---

## 📝 Railway Configuration Explained

### **Procfile**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```
- `web`: Process type
- `uvicorn main:app`: Run FastAPI app dari `main.py`
- `--host 0.0.0.0`: Listen on all interfaces
- `--port $PORT`: Use Railway's assigned port

### **railway.toml**
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```
- Specify Nixpacks builder
- Override start command

### **nixpacks.toml**
```toml
[phases.setup]
nixPkgs = ["python310", "ffmpeg"]
```
- Install Python 3.10
- Install ffmpeg (required by yt-dlp)

---

## 🧪 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Or with uvicorn
uvicorn main:app --reload --port 8000

# Test
curl http://localhost:8000/
curl "http://localhost:8000/api/analyze?username=kaycee"
```

---

## 🎯 Expected Response

### **Health Check (`GET /`)**
```json
{
  "success": true,
  "message": "TikTok API is running",
  "version": "1.0.0",
  "endpoints": {
    "analyze": "/api/analyze?username=<username>"
  }
}
```

### **Analyze User (`GET /api/analyze?username=kaycee`)**
```json
{
  "success": true,
  "username": "kaycee",
  "video_count": 30,
  "data": [
    {
      "id": "7123456789",
      "title": "Video Title",
      "views": 1000000,
      "likes": 50000,
      "comments": 1000,
      "shares": 500,
      "cover": "https://...",
      "playUrl": "https://www.tiktok.com/@kaycee/video/7123456789",
      "create_time": 1234567890
    }
  ]
}
```

---

## 🔒 Security Notes

- No API keys required
- CORS enabled for all origins (adjust in production)
- Rate limiting: Consider adding if needed

---

## 📊 Monitoring

Railway provides:
- Real-time logs
- Metrics (CPU, Memory, Network)
- Deployment history

Access via Railway Dashboard → Your Project → Logs/Metrics

---

## 💰 Railway Pricing

**Free Tier:**
- $5 credit per month
- ~500 hours runtime
- Enough for development/testing

**Pro Plan:**
- $20/month
- Unlimited projects
- Better performance

---

## ✅ Deployment Checklist

- [x] `main.py` exists at root
- [x] `requirements.txt` with versions
- [x] `Procfile` with correct command
- [x] `railway.toml` configured
- [x] `nixpacks.toml` with ffmpeg
- [x] `runtime.txt` with Python version
- [x] Code pushed to GitHub
- [x] Railway project created
- [x] Domain generated
- [x] Endpoints tested

---

**Sekarang deploy ulang dan seharusnya berhasil!** 🚀
