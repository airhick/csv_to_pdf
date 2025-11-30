# 🚀 Deploy to Render - Quick Guide

Deploy your PDF Generator API to Render in **5 minutes** and get a permanent public URL.

## 📋 Prerequisites

- A [Render account](https://render.com) (free tier available)
- Your code pushed to GitHub/GitLab/Bitbucket (or use Render's direct deploy)

## 🎯 Method 1: Deploy via Render Dashboard (Recommended)

### Step 1: Prepare Your Repository

Make sure your code is in a Git repository (GitHub, GitLab, or Bitbucket).

**Required files:**
- ✅ `app.py` - Your Flask application
- ✅ `requirements.txt` - Python dependencies
- ✅ `recto.pdf` or `rescto.pdf` - Default PDF template (optional, can upload via API)
- ✅ `render.yaml` - Render configuration (optional but recommended)

### Step 2: Create a New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your repository (GitHub/GitLab/Bitbucket)
4. Select your repository and branch

### Step 3: Configure the Service

**Basic Settings:**
- **Name:** `pdf-generator-api` (or any name you prefer)
- **Region:** Choose closest to you
- **Branch:** `main` (or your default branch)
- **Root Directory:** Leave empty (or `.` if your files are in a subdirectory)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`

**Environment Variables:**
Click **"Advanced"** → **"Add Environment Variable"** and add:

| Key | Value | Notes |
|-----|-------|-------|
| `PORT` | `8002` | Port for the app (Render will override with actual port) |
| `HOST` | `0.0.0.0` | Listen on all interfaces |
| `DEBUG` | `false` | Disable debug mode in production |
| `REQUIRE_API_KEY` | `true` | Enable API key protection |
| `API_KEY` | `your-secret-key-here` | **Generate a secure key** (see below) |

**Generate a secure API key:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Install dependencies
   - Build your application
   - Start the service
3. Wait 2-3 minutes for the first deployment

### Step 5: Get Your Public URL

Once deployed, Render will provide you with a URL like:
```
https://pdf-generator-api.onrender.com
```

**Your API endpoints:**
- Web UI: `https://pdf-generator-api.onrender.com/`
- Health Check: `https://pdf-generator-api.onrender.com/health`
- API Generate: `https://pdf-generator-api.onrender.com/api/generate`

---

## 🎯 Method 2: Deploy via render.yaml (Automatic)

If you have `render.yaml` in your repository, Render will automatically detect it.

### Step 1: Push render.yaml to your repo

The `render.yaml` file is already created in your project. Just commit and push:

```bash
git add render.yaml
git commit -m "Add Render configuration"
git push
```

### Step 2: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your repository
4. Render will detect `render.yaml` and pre-fill all settings
5. **Important:** Set your `API_KEY` environment variable:
   - Go to your service → **Environment** tab
   - Add `API_KEY` with a secure value (generate one as shown above)
6. Click **"Apply"** to deploy

---

## 🔧 Configuration Details

### Port Configuration

Your `app.py` already handles Render's port correctly:
```python
port = int(os.environ.get('PORT', 8002))
```

Render automatically sets the `PORT` environment variable, so your app will work out of the box.

### Default PDF Template

The app looks for `recto.pdf` or `rescto.pdf` in the root directory. Make sure to:
- Include one of these files in your repository, OR
- Always upload a PDF template via the API/web interface

### File Upload Limits

Render free tier has a **100MB** request body limit. For large PDFs:
- Use the JSON API mode (more efficient)
- Process files in batches
- Consider upgrading to a paid plan for higher limits

---

## 🧪 Testing Your Deployment

### Test 1: Health Check

```bash
curl https://your-app.onrender.com/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "PDF Generator API",
  "version": "2.1"
}
```

### Test 2: API Generate (with API Key)

```bash
curl -X POST https://your-app.onrender.com/api/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "name": "Test User",
        "address": "123 Test Street\nTest City\nTest Country"
      }
    ],
    "singleFile": true
  }' \
  -o test.pdf
```

### Test 3: Web Interface

Open in browser:
```
https://your-app.onrender.com/
```

You should see the web interface for uploading CSV and PDF files.

---

## 🔒 Security Best Practices

1. **Always use API Key protection** in production:
   - Set `REQUIRE_API_KEY=true`
   - Use a strong, randomly generated `API_KEY`
   - Never commit API keys to Git

2. **HTTPS is automatic** on Render (all traffic is encrypted)

3. **Monitor your service:**
   - Check Render dashboard for logs
   - Monitor usage and costs
   - Set up alerts for errors

---

## 📊 Render Plans

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0/month | 750 hours/month, sleeps after 15min inactivity |
| **Starter** | $7/month | Always on, 512MB RAM, 0.5 CPU |
| **Standard** | $25/month | Always on, 2GB RAM, 1 CPU |

**For production use:** Consider Starter plan to avoid cold starts.

---

## 🐛 Troubleshooting

### Service won't start

**Check logs:**
1. Go to Render dashboard → Your service → **Logs** tab
2. Look for Python errors or import issues

**Common issues:**
- Missing dependencies in `requirements.txt`
- Port configuration (should use `PORT` env var)
- Missing files (check `recto.pdf` or `rescto.pdf`)

### "502 Bad Gateway" or service sleeping

**Free tier limitation:**
- Services sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- **Solution:** Upgrade to Starter plan ($7/month) for always-on

### API Key not working

**Verify:**
1. Check `REQUIRE_API_KEY` is set to `true`
2. Verify `API_KEY` environment variable is set correctly
3. Use the exact key in your requests (check for extra spaces)

### Large file uploads fail

**Render limits:**
- Free/Starter: 100MB request body limit
- **Solution:** 
  - Use JSON API mode (more efficient)
  - Split large batches into smaller requests
  - Upgrade plan for higher limits

---

## 🔄 Updating Your Deployment

### Automatic Deploys (Recommended)

Render automatically deploys when you push to your connected branch:
```bash
git add .
git commit -m "Update app"
git push
```

Render will detect the push and redeploy automatically.

### Manual Deploy

1. Go to Render dashboard → Your service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 📝 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | ✅ | `8002` | Port to listen on (Render sets this automatically) |
| `HOST` | ❌ | `0.0.0.0` | Host to bind to |
| `DEBUG` | ❌ | `false` | Enable Flask debug mode |
| `REQUIRE_API_KEY` | ❌ | `false` | Require API key for `/api/generate` |
| `API_KEY` | ⚠️ | `None` | Secret API key (required if `REQUIRE_API_KEY=true`) |

---

## 🎉 You're Done!

Your API is now accessible at:
```
https://your-app.onrender.com
```

**Use this URL in:**
- n8n workflows
- Zapier integrations
- Custom applications
- Any HTTP client

**Example API call:**
```bash
curl -X POST https://your-app.onrender.com/api/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": [{"name": "Test", "address": "123 Main St"}]}'
```

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-flask)
- [API Documentation](./API_DOCUMENTATION.md)
- [API Examples](./API_EXAMPLES.py)

---

**Need help?** Check the logs in Render dashboard or review the troubleshooting section above.

