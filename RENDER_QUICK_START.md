# ⚡ Render Quick Start - 3 Steps

Deploy your PDF API to Render in **3 minutes** and get a permanent public URL.

## 🚀 Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push
```

## 🚀 Step 2: Deploy on Render

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your repo and branch
5. Render will auto-detect settings from `render.yaml`

**Configure:**
- **Name:** `pdf-generator-api` (or any name)
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`

**Add Environment Variable:**
- Go to **"Environment"** tab
- Add: `API_KEY` = `your-secret-key-here`
  - Generate one: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`

6. Click **"Create Web Service"**

## 🚀 Step 3: Get Your URL

Wait 2-3 minutes, then your API will be live at:
```
https://your-app-name.onrender.com
```

**Test it:**
```bash
curl https://your-app-name.onrender.com/health
```

**Use your API:**
```bash
curl -X POST https://your-app-name.onrender.com/api/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": [{"name": "Test", "address": "123 Main St"}], "singleFile": true}' \
  -o test.pdf
```

## ✅ Done!

Your API is now accessible from anywhere in the world.

**Full guide:** See `DEPLOY_RENDER.md` for detailed instructions and troubleshooting.

