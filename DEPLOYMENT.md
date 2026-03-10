# MixDrink Deployment Guide

## Overview

This guide covers deploying MixDrink to production:
- **Frontend**: Vercel (React/Vite app)
- **Backend**: Railway (FastAPI + PostgreSQL)

## Option 1: Quick Deploy (Recommended)

### Step 1: Deploy Backend to Railway

1. **Create Railway Account**: https://railway.app/

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub and select the mixdrink repo
   - Choose "Deploy from monorepo" → Select `backend` folder

3. **Add PostgreSQL**:
   - In your Railway project, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically create a DATABASE_URL

4. **Configure Environment Variables**:
   - In Railway project settings → Variables
   - Add these variables:
     ```
     ANTHROPIC_API_KEY=sk-ant-your-key-here
     DATABASE_URL=${{Postgres.DATABASE_URL}}  (Railway auto-fills this)
     CORS_ORIGINS=["https://your-vercel-app.vercel.app"]
     CLAUDE_MODEL=claude-sonnet-4-5
     MAX_TOKENS=4096
     ```

5. **Configure Start Command**:
   - In Railway settings → Deploy
   - Start Command: `alembic upgrade head && python seed.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: `backend`

6. **Deploy**:
   - Railway will auto-deploy
   - Note your backend URL (e.g., `https://mixdrink-backend.up.railway.app`)

### Step 2: Deploy Frontend to Vercel

1. **Install Vercel CLI** (if not installed):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy Frontend**:
   ```bash
   cd /Users/ydauber/Build/claude/mixdrink/frontend
   vercel
   ```

   When prompted:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - Project name? **mixdrink** (or your choice)
   - Directory? `.` (current directory)
   - Override settings? **Y**
   - Build Command? `npm run build`
   - Output Directory? `dist`
   - Development Command? `npm run dev`

4. **Set Environment Variable**:
   ```bash
   vercel env add VITE_API_URL
   ```
   Enter your Railway backend URL: `https://your-backend.up.railway.app`

5. **Redeploy with env var**:
   ```bash
   vercel --prod
   ```

### Step 3: Update CORS

Go back to Railway and update the CORS_ORIGINS variable with your Vercel URL:
```
CORS_ORIGINS=["https://your-app.vercel.app"]
```

Railway will auto-redeploy.

### Step 4: Verify Deployment

1. Visit your Vercel URL
2. Check if drinks load from the backend
3. Test search/filter
4. Test consuming drinks
5. Test AI recommendations

---

## Option 2: GitHub Integration (Automated)

### 1. Push to GitHub

```bash
cd /Users/ydauber/Build/claude/mixdrink
git init
git add .
git commit -m "Initial commit: MixDrink app"
gh repo create mixdrink --public --source=. --remote=origin --push
```

### 2. Deploy Backend via Railway GitHub Integration

1. Go to Railway.app
2. "New Project" → "Deploy from GitHub repo"
3. Select your mixdrink repository
4. Railway will detect the monorepo
5. Configure as described in Option 1

### 3. Deploy Frontend via Vercel GitHub Integration

1. Go to vercel.com
2. "Add New..." → "Project"
3. Import your GitHub repository
4. Vercel will detect the frontend
5. Configure:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Add environment variable: `VITE_API_URL` = your Railway backend URL
7. Deploy

---

## Option 3: Alternative Backend Hosts

### Deploy to Render.com

1. Create account at render.com
2. New Web Service
3. Connect GitHub repo
4. Configure:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `alembic upgrade head && python seed.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add PostgreSQL database
6. Add environment variables

### Deploy to Fly.io

```bash
cd backend
flyctl launch
flyctl secrets set ANTHROPIC_API_KEY=your-key
flyctl deploy
```

---

## Environment Variables Reference

### Backend (Railway/Render/Fly)
```
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://...  (auto-provided by host)
CORS_ORIGINS=["https://your-vercel-app.vercel.app"]
CLAUDE_MODEL=claude-sonnet-4-5
MAX_TOKENS=4096
```

### Frontend (Vercel)
```
VITE_API_URL=https://your-backend.up.railway.app
```

---

## Troubleshooting

### Frontend can't reach backend
- Check CORS_ORIGINS includes your Vercel URL
- Verify VITE_API_URL is set correctly in Vercel
- Check Railway/Render logs for errors

### Database migrations not running
- Ensure start command includes `alembic upgrade head`
- Check Railway/Render logs for migration errors

### No drinks appearing
- Ensure seed command runs: `python seed.py`
- Check if DATABASE_URL is correctly set
- View backend logs

### AI recommendations not working
- Verify ANTHROPIC_API_KEY is set in backend environment
- Check API key is valid at console.anthropic.com
- Review backend logs for API errors

---

## Production Checklist

- [ ] Backend deployed to Railway/Render/Fly
- [ ] PostgreSQL database created
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] Database seeded (`python seed.py`)
- [ ] All backend environment variables set
- [ ] Backend health check working (`/api/health`)
- [ ] Frontend deployed to Vercel
- [ ] Frontend environment variable set (VITE_API_URL)
- [ ] CORS updated with production frontend URL
- [ ] Test: Browse drinks
- [ ] Test: Search/filter
- [ ] Test: Consume drinks
- [ ] Test: Get recommendations
- [ ] Test: Reset session

---

## Costs

**Free Tier Limits:**
- **Vercel**: Free for personal projects
- **Railway**: $5/month free credit (hobby plan)
- **Render**: Free tier available (with limitations)
- **Anthropic API**: Pay-per-use (Claude Sonnet ~$3 per million tokens)

Estimated monthly cost for low traffic: **$0-10**

---

**Need help?** Check the logs in Railway/Render dashboard and Vercel deployment logs.
