# 🍸 MixDrink - AI-Powered Drink Pairing App

A clean, mobile-friendly web app that recommends alcoholic drink pairings based on what you've already consumed.

## 🌐 Live Demo

**App:** https://frontend-one-nu-40.vercel.app
**API:** https://backend-eta-sooty-41.vercel.app

## ✨ Features

- **Simple Interface**: Type or search for drinks you've had
- **AI-Powered Recommendations**: Get smart pairing suggestions using Claude AI
- **Three Categories of Recommendations**:
  - ✨ **Great Combinations** - Excellent pairings that complement what you've had
  - 👍 **Okay Combinations** - Acceptable pairings that won't clash
  - ⚠️ **Not Recommended** - Combinations to avoid
- **Short Explanations**: Each recommendation includes reasoning
- **Mobile-Friendly**: Modern, responsive design
- **Reset Button**: Start over anytime

## 🚀 How to Use

1. Visit https://frontend-one-nu-40.vercel.app
2. Search and select drinks you've consumed (e.g., "Whiskey", "Red Wine")
3. Click "Get Pairing Recommendations"
4. View categorized recommendations with explanations
5. Click "Start Over" to reset

## 🛠️ Tech Stack

**Frontend:**
- React 19 + TypeScript
- Vite
- Tailwind CSS
- Lucide Icons

**Backend:**
- FastAPI (Python)
- PostgreSQL (Vercel Postgres)
- Anthropic Claude API
- SQLAlchemy (async)

**Deployment:**
- Vercel (Frontend & Backend)
- Vercel Postgres (Database)

## 🔑 Environment Variables

### Backend (Vercel)
- `ANTHROPIC_API_KEY` - Claude API key (⚠️ needs credits for AI recommendations)
- `POSTGRES_URL` - Database connection (auto-set by Vercel)
- `CORS_ORIGINS` - Allowed origins (JSON array)

### Frontend (Vercel)
- `VITE_API_URL` - Backend API URL

## 🤖 AI Fallback

If the Anthropic API is unavailable or credits are low, the app automatically falls back to rule-based recommendations.

## 📄 License

MIT
