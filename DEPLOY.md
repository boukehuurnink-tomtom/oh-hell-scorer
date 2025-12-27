# Deployment Guide - Oh Hell Score Recorder

This guide covers several easy ways to deploy your Oh Hell Score Recorder to the web.

---

## Option 1: Railway.app (Recommended - Easiest)

**Free tier available, automatic deployments from GitHub**

### Steps:

1. **Sign up at [Railway.app](https://railway.app)**
   - Use your GitHub account to sign in

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `oh-hell-scorer` repository

3. **Railway will auto-detect Flask**
   - It will use your `Procfile` and `requirements.txt`
   - No additional configuration needed

4. **Generate Domain**
   - Click on your deployment
   - Go to "Settings" → "Networking"
   - Click "Generate Domain"
   - Your app will be live at: `https://your-app.up.railway.app`

**Benefits:**
- ✅ Free tier (500 hours/month)
- ✅ Automatic deployments on git push
- ✅ HTTPS included
- ✅ Very fast setup (~2 minutes)

---

## Option 2: Render.com

**Free tier available, similar to Railway**

### Steps:

1. **Sign up at [Render.com](https://render.com)**

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select `oh-hell-scorer`

3. **Configure:**
   - **Name:** oh-hell-scorer
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free

4. **Deploy**
   - Click "Create Web Service"
   - Your app will be live at: `https://oh-hell-scorer.onrender.com`

**Benefits:**
- ✅ Free tier
- ✅ Auto-deploy on push
- ✅ HTTPS included
- ✅ Great documentation

**Note:** Free tier spins down after inactivity (first load may be slow)

---

## Option 3: Heroku

**Classic platform, reliable**

### Steps:

1. **Install Heroku CLI**
   ```bash
   brew install heroku/brew/heroku
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   cd /path/to/oh-hell-scorer
   heroku create your-app-name
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

**Benefits:**
- ✅ Very mature platform
- ✅ Extensive documentation
- ✅ Easy rollbacks

**Note:** Free tier ended in 2022, now starts at $5/month

---

## Option 4: Python Anywhere

**Python-focused hosting**

### Steps:

1. **Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)**

2. **Upload your code:**
   - Use their file manager or git
   - Clone from GitHub: `git clone https://github.com/boukehuurnink-tomtom/oh-hell-scorer`

3. **Create Web App:**
   - Dashboard → Web → Add new web app
   - Choose Flask
   - Point to your `app.py`

4. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Reload web app**
   - Your app will be at: `https://yourusername.pythonanywhere.com`

**Benefits:**
- ✅ Free tier available
- ✅ Python-specific platform
- ✅ Good for learning

---

## Option 5: Vercel (Serverless)

**Modern serverless platform**

### Additional Setup Required:

Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Steps:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   cd /path/to/oh-hell-scorer
   vercel
   ```

3. **Follow prompts**
   - Link to your account
   - Deploy!

**Benefits:**
- ✅ Free tier
- ✅ Very fast (CDN)
- ✅ Automatic HTTPS

**Note:** Session storage may not work well (serverless functions are stateless)

---

## Recommended Configuration

### For session persistence across deployments:

Consider using Redis for session storage instead of server-side sessions.

Add to `requirements.txt`:
```
redis==5.0.1
Flask-Session==0.5.0
```

Update `app.py`:
```python
from flask_session import Session
import redis

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379'))
Session(app)
```

Most platforms (Railway, Render) offer free Redis add-ons.

---

## My Recommendation: Railway.app

**Why Railway?**
- Free tier is generous
- Auto-deploys from GitHub
- Fast and reliable
- Great developer experience
- No credit card required for free tier

**Setup time:** ~2 minutes

---

## Custom Domain (Optional)

All platforms above support custom domains:

1. **Purchase domain** (Namecheap, Google Domains, etc.)
2. **Add CNAME record:**
   - Point to your Railway/Render/Heroku URL
3. **Configure in platform settings**
4. **Wait for DNS propagation** (5-60 minutes)

---

## Environment Variables

If you need environment variables (for production settings):

### Railway/Render/Heroku:
- Go to Settings → Environment Variables
- Add: `FLASK_ENV=production`

### In your code:
```python
import os
app.config['ENV'] = os.environ.get('FLASK_ENV', 'development')
```

---

## Monitoring & Logs

All platforms provide:
- ✅ Real-time logs
- ✅ Metrics (CPU, memory)
- ✅ Deployment history
- ✅ Rollback capability

---

## Summary

| Platform | Free Tier | Setup Time | Best For |
|----------|-----------|------------|----------|
| **Railway** | ✅ 500hrs | 2 min | Beginners |
| **Render** | ✅ Yes | 3 min | Free hosting |
| **Heroku** | ❌ $5/mo | 5 min | Production |
| **PythonAnywhere** | ✅ Limited | 10 min | Learning |
| **Vercel** | ✅ Yes | 3 min | Serverless |

**Start with Railway.app** - it's the easiest and most reliable for this app! 🚀
