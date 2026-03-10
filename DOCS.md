# 📚 MixDrink Documentation

Welcome to the MixDrink documentation! This guide will help you navigate all available documentation.

## 🗂️ Documentation Index

### For Users

- **[README.md](README.md)** - Main project documentation
  - Project overview and features
  - Tech stack details
  - Installation instructions
  - Usage guide and examples
  - API reference
  - Contributing guidelines

### For Developers

- **[CLAUDE.md](CLAUDE.md)** - Comprehensive technical documentation for AI agents
  - Complete project architecture
  - Database schema and patterns
  - Backend and frontend patterns
  - Development workflow
  - API endpoint details
  - Performance optimization
  - Security considerations
  - Future enhancements roadmap

### For Deployment

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide
  - Step-by-step Vercel deployment (current production setup)
  - Environment variables configuration
  - Database setup with Vercel Postgres
  - Troubleshooting guide
  - Production checklist
  - Alternative deployment options (Railway, Render, Fly.io)

### Additional Files

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide for local development
- **[.env.example](backend/.env.example)** - Backend environment variables template
- **[.env.example](frontend/.env.example)** - Frontend environment variables template

## 🚀 Quick Links

### Live Application
- **App**: https://frontend-one-nu-40.vercel.app
- **API**: https://backend-eta-sooty-41.vercel.app
- **API Docs**: https://backend-eta-sooty-41.vercel.app/docs

### External Resources
- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vercel Documentation](https://vercel.com/docs)

## 📖 Documentation by Use Case

### "I want to understand the project"
→ Start with **[README.md](README.md)**

### "I want to develop locally"
→ Read **[QUICKSTART.md](QUICKSTART.md)** or **[README.md#installation](README.md#installation)**

### "I want to deploy to production"
→ Follow **[DEPLOYMENT.md](DEPLOYMENT.md)**

### "I'm an AI agent working on this project"
→ Read **[CLAUDE.md](CLAUDE.md)** for complete technical details

### "I want to contribute"
→ See **[README.md#contributing](README.md#contributing)** and **[CLAUDE.md#development-workflow](CLAUDE.md#development-workflow)**

### "I'm troubleshooting an issue"
→ Check **[DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)**

## 🏗️ Project Structure Overview

```
mixdrink/
├── DOCS.md                    # This file - documentation index
├── README.md                  # User-facing documentation
├── CLAUDE.md                  # Technical documentation for AI agents
├── DEPLOYMENT.md              # Deployment guide
├── QUICKSTART.md              # Quick start guide
│
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── api/routes/       # API endpoints
│   │   ├── db/               # Database models
│   │   ├── services/         # Business logic
│   │   ├── models/           # Pydantic schemas
│   │   ├── config.py         # Configuration
│   │   └── main.py           # App entry point
│   ├── requirements.txt       # Python dependencies
│   ├── vercel.json           # Vercel config
│   └── .env.example          # Environment template
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── stores/           # Zustand stores
│   │   ├── services/         # API client
│   │   └── types/            # TypeScript types
│   ├── package.json          # Node dependencies
│   ├── vite.config.ts        # Vite configuration
│   ├── vercel.json           # Vercel config
│   └── .env.example          # Environment template
│
└── docker-compose.yml         # Local PostgreSQL setup
```

## 🎯 Key Concepts

### Tech Stack
- **Backend**: FastAPI (Python) + PostgreSQL + Claude AI
- **Frontend**: React 19 + TypeScript + Zustand + ReactFlow
- **Infrastructure**: Vercel (serverless) + Vercel Postgres

### Core Features
1. **Drink Library** - Browse and search 77+ drinks
2. **Session Tracking** - Visual timeline of consumption
3. **AI Recommendations** - Claude-powered suggestions
4. **Session Management** - Track drinking sessions

### Architecture
- **Backend**: Layered architecture (Routes → Services → Database)
- **Frontend**: Component composition with centralized state
- **Database**: Async SQLAlchemy ORM with PostgreSQL
- **AI**: Anthropic Claude API for recommendations

## 📝 Documentation Standards

### For Contributors

When adding documentation:
1. **README.md** - User-facing features and quick start
2. **CLAUDE.md** - Technical implementation details
3. **DEPLOYMENT.md** - Deployment and operations
4. Keep examples current and tested
5. Update this index when adding new docs

### Documentation Principles
- ✅ Clear and concise
- ✅ Examples and code snippets
- ✅ Up-to-date with latest changes
- ✅ Accessible to different skill levels
- ✅ Well-organized and searchable

## 🆘 Getting Help

1. **Check documentation** - Start with this index
2. **Search existing issues** - GitHub Issues
3. **Review API docs** - `/docs` endpoint
4. **Check logs** - Vercel dashboard
5. **Ask for help** - Create a GitHub issue

## 🔄 Keeping Documentation Updated

Documentation is updated when:
- New features are added
- Architecture changes
- Deployment process changes
- Breaking changes occur
- Community feedback suggests improvements

Last updated: March 2026

## ⭐ Quick Reference

| Task | Command |
|------|---------|
| Start backend locally | `uvicorn app.main:app --reload` |
| Start frontend locally | `npm run dev` |
| Deploy backend | `vercel --prod` (from backend/) |
| Deploy frontend | `vercel --prod` (from frontend/) |
| Initialize database | `curl -X POST <backend-url>/api/init-db` |
| View API docs | Visit `<backend-url>/docs` |

---

**Need something not covered here?** Open an issue or submit a PR to improve the docs!

**Built with 📚 by the MixDrink team**
