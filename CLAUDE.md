# MixDrink - AI-Powered Drink Pairing Platform

## Project Overview

MixDrink is an interactive web application that helps users discover drink pairings and track their drinking sessions with AI-powered recommendations from Claude. The app provides intelligent suggestions based on flavor profiles, alcohol pacing, and palate cleansing.

**Live App**: https://frontend-one-nu-40.vercel.app
**API**: https://backend-eta-sooty-41.vercel.app
**Docs**: https://backend-eta-sooty-41.vercel.app/docs

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework for serverless functions
- **PostgreSQL** - Vercel Postgres database
- **SQLAlchemy** (async) - Async ORM for database operations
- **Anthropic Claude API** - AI-powered drink recommendations
- **Pydantic** - Data validation and settings management

### Frontend
- **React 19** - UI framework with TypeScript
- **Vite** - Build tool and dev server
- **Zustand** - Lightweight state management
- **ReactFlow** - Interactive flow diagrams for session visualization
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API calls

### Infrastructure
- **Vercel** - Serverless deployment for frontend and backend
- **Vercel Postgres** - Managed PostgreSQL database (free tier)
- **GitHub** - Source control

## Project Structure

```
mixdrink/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/        # API route handlers
│   │   │       ├── drinks.py      # Drink catalog endpoints
│   │   │       ├── session.py     # Session management
│   │   │       └── recommendations.py  # AI recommendations
│   │   ├── db/
│   │   │   ├── database.py    # Database connection & session
│   │   │   ├── models.py      # SQLAlchemy ORM models
│   │   │   └── seed_data.py   # Initial drink data
│   │   ├── models/
│   │   │   └── schemas.py     # Pydantic schemas
│   │   ├── services/          # Business logic layer
│   │   │   ├── drink_service.py
│   │   │   ├── session_service.py
│   │   │   └── recommendation_service.py
│   │   ├── config.py          # Settings and configuration
│   │   └── main.py            # FastAPI app entry point
│   ├── api/
│   │   └── index.py           # Vercel serverless entry
│   ├── requirements.txt       # Python dependencies
│   ├── vercel.json           # Vercel deployment config
│   └── .env.example          # Environment variables template
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── DrinkLibrary.tsx       # Drink browsing
│   │   │   ├── DrinkCard.tsx          # Individual drink display
│   │   │   ├── DrinkFlowDiagram.tsx   # Session visualization
│   │   │   ├── SessionControls.tsx    # Session management
│   │   │   └── RecommendationPanel.tsx # AI suggestions
│   │   ├── stores/           # Zustand state stores
│   │   │   ├── drinkStore.ts
│   │   │   └── sessionStore.ts
│   │   ├── services/
│   │   │   └── api.ts        # API client
│   │   ├── types/
│   │   │   └── index.ts      # TypeScript types
│   │   └── App.tsx           # Main app component
│   ├── package.json
│   ├── vite.config.ts
│   ├── vercel.json           # Vercel deployment config
│   └── .env.example          # Environment variables template
│
├── CLAUDE.md                 # This file - AI agent instructions
├── README.md                 # User-facing documentation
└── DEPLOYMENT.md             # Deployment guide
```

## Database Schema

### Drink Table
```sql
CREATE TABLE drink (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,  -- spirit, cocktail, wine, beer, liqueur
    subcategory VARCHAR(50),
    alcohol_content DECIMAL(4,2),   -- ABV percentage
    flavor_profile JSONB,           -- {sweet, bitter, sour, savory, fruity}
    description TEXT,
    base_spirit VARCHAR(50),
    ingredients JSONB,              -- Array of ingredients
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### DrinkSession Table
```sql
CREATE TABLE drink_session (
    id SERIAL PRIMARY KEY,
    session_name VARCHAR(100),
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### ConsumedDrink Table
```sql
CREATE TABLE consumed_drink (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES drink_session(id),
    drink_id INTEGER REFERENCES drink(id),
    consumed_at TIMESTAMP DEFAULT NOW(),
    drink_order INTEGER,
    notes TEXT
);
```

## Architecture Patterns

### Backend Patterns

#### 1. **Layered Architecture**
```
Routes (API Layer) → Services (Business Logic) → Database (Data Layer)
```

- **Routes**: Handle HTTP requests/responses, validation, and error handling
- **Services**: Contain business logic and orchestrate database operations
- **Models**: Define database schema and Pydantic validation

#### 2. **Async/Await Pattern**
All database operations use async/await for better performance:
```python
async def get_drinks(db: AsyncSession, search: str = None):
    query = select(Drink)
    if search:
        query = query.where(Drink.name.ilike(f"%{search}%"))
    result = await db.execute(query)
    return result.scalars().all()
```

#### 3. **Dependency Injection**
FastAPI's dependency system for database sessions:
```python
@router.get("/drinks")
async def get_drinks(db: AsyncSession = Depends(get_db)):
    drinks = await drink_service.get_drinks(db)
    return drinks
```

#### 4. **Configuration Management**
Centralized settings with environment variables:
```python
class Settings(BaseSettings):
    anthropic_api_key: str
    database_url: str
    cors_origins: str

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### Frontend Patterns

#### 1. **State Management with Zustand**
Simple, performant state management:
```typescript
export const useSessionStore = create<SessionState>((set) => ({
  currentSession: null,
  consumedDrinks: [],
  loadCurrentSession: async () => {
    const session = await sessionApi.getCurrentSession();
    set({ currentSession: session, consumedDrinks: session.drinks });
  },
}));
```

#### 2. **API Service Layer**
Centralized API calls:
```typescript
export const drinkApi = {
  getDrinks: async (filters?: DrinkFilters): Promise<Drink[]> => {
    const response = await api.get<Drink[]>('/api/drinks', { params: filters });
    return response.data;
  },
};
```

#### 3. **Component Composition**
Modular, reusable components:
```
App
├── DrinkLibrary (sidebar)
├── DrinkFlowDiagram (center)
└── RecommendationPanel (sidebar)
```

## API Endpoints

### Drinks API
```
GET  /api/drinks              # List all drinks with filters
GET  /api/drinks/{id}         # Get specific drink
GET  /api/drinks/categories   # List unique categories
```

### Session API
```
POST   /api/session/start     # Start new session
GET    /api/session/current   # Get active session
POST   /api/session/consume   # Add drink to session
DELETE /api/session/reset     # End current, start new
GET    /api/session/history   # Get past sessions
```

### AI Recommendations API
```
POST /api/recommendations     # Get AI drink suggestions
```

### Utility Endpoints
```
GET  /api/health              # Health check
POST /api/init-db             # Initialize database (one-time)
GET  /docs                    # OpenAPI documentation
```

## Development Workflow

### Local Development

#### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Start development server
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000

#### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.example .env
# Edit .env to point to backend

# Start development server
npm run dev
```

Frontend runs at: http://localhost:5173

### Testing

#### Backend Testing
```bash
cd backend
pytest
```

#### Frontend Testing
```bash
cd frontend
npm run lint
npm run build  # Test production build
```

### Common Development Tasks

#### Add a New Drink
Edit `backend/app/db/seed_data.py` and add to `DRINKS_DATA`:
```python
{
    "name": "New Drink",
    "category": "cocktail",
    "subcategory": "classic",
    "alcohol_content": 15.0,
    "flavor_profile": {"sweet": 3, "bitter": 2, ...},
    "description": "Description here",
    "ingredients": ["Ingredient 1", "Ingredient 2"]
}
```

Then re-run the seed script or call `/api/init-db` endpoint.

#### Modify AI Recommendations
Edit `backend/app/services/recommendation_service.py`:
- Update system prompt for different recommendation styles
- Modify scoring logic for drink selection
- Adjust context sent to Claude

#### Add New API Endpoint
1. Create route in `backend/app/api/routes/`
2. Add business logic in `backend/app/services/`
3. Register router in `backend/app/main.py`
4. Update frontend API client in `frontend/src/services/api.ts`

## Deployment

### Vercel Deployment (Current Setup)

**Prerequisites:**
- Vercel account (free tier)
- Vercel CLI: `npm install -g vercel`

#### Backend Deployment
```bash
cd backend
vercel --prod
```

**Environment Variables (set in Vercel dashboard):**
- `ANTHROPIC_API_KEY` - Your Claude API key
- `POSTGRES_URL` - Auto-added by Vercel Postgres
- `CORS_ORIGINS` - Frontend URL in JSON array format
- `CLAUDE_MODEL` - `claude-sonnet-4-5`
- `MAX_TOKENS` - `4096`

#### Frontend Deployment
```bash
cd frontend
vercel --prod
```

**Environment Variables:**
- `VITE_API_URL` - Backend URL (e.g., https://backend-xxx.vercel.app)

#### Database Setup
1. Go to Vercel Dashboard → Storage → Create Database → Postgres
2. Connect to backend project
3. Call `/api/init-db` endpoint to initialize tables and seed data

### Current Production URLs
- Frontend: https://frontend-one-nu-40.vercel.app
- Backend: https://backend-eta-sooty-41.vercel.app

## AI Integration Details

### Claude API Usage

The app uses Claude for intelligent drink recommendations based on:

1. **Flavor Progression**: Building complementary flavors or creating contrasts
2. **Alcohol Pacing**: Preventing rapid ABV increases
3. **Palate Cleansing**: Recommending variety in base spirits
4. **Session Context**: Time, drink count, and total alcohol consumption

### Recommendation Service

Located in `backend/app/services/recommendation_service.py`:

```python
async def get_recommendations(session_with_drinks):
    # Build context from session history
    context = build_context(session_with_drinks)

    # Call Claude API
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": context}]
    )

    # Parse and return suggestions
    return parse_recommendations(message.content)
```

### Prompt Engineering

**System Prompt** (excerpt):
```
You are an expert mixologist and sommelier helping users discover
great drink pairings. Analyze their drinking session and suggest
3 drinks that would pair well based on:

1. Flavor progression (complementary or contrasting)
2. Alcohol pacing (avoid rapid ABV spikes)
3. Palate cleansing (vary base spirits)
4. Overall session context
```

## Security Considerations

### API Keys
- Never commit `.env` files to git
- Use environment variables for all secrets
- Rotate API keys regularly

### Database
- Use parameterized queries (SQLAlchemy ORM handles this)
- Validate all user input with Pydantic schemas
- Enable SSL for production database connections

### CORS
- Restrict `CORS_ORIGINS` to specific frontend domains
- Never use `["*"]` in production

### Rate Limiting
Consider adding rate limiting for:
- AI recommendation endpoint (expensive)
- Database write operations
- Public API endpoints

## Troubleshooting

### Backend Issues

**Database connection errors:**
- Check `POSTGRES_URL` environment variable
- Verify database is running
- Check SSL/connection parameters

**Claude API errors:**
- Verify `ANTHROPIC_API_KEY` is set correctly
- Check API quota and billing
- Review error logs in Vercel

### Frontend Issues

**Network errors:**
- Check `VITE_API_URL` points to correct backend
- Verify CORS is configured correctly
- Check browser console for errors

**Drinks not loading:**
- Verify backend `/api/drinks` endpoint works
- Check database has been seeded
- Inspect network tab in browser DevTools

### Deployment Issues

**Vercel serverless timeout:**
- Optimize database queries
- Consider caching for expensive operations
- Break down long-running tasks

**Cold start latency:**
- Accept 1-2 second initial load time
- Implement loading states in frontend
- Consider Vercel's always-on features for production

## Performance Optimization

### Backend
- Use database indexes on frequently queried columns
- Implement query result caching
- Optimize AI prompt length to reduce API costs
- Use connection pooling for database

### Frontend
- Lazy load components
- Implement virtual scrolling for large lists
- Cache API responses in Zustand store
- Optimize images and assets

## Future Enhancements

### Planned Features
- [ ] User authentication and profiles
- [ ] Save and share drinking sessions
- [ ] Custom drink creation
- [ ] Social features (share with friends)
- [ ] Mobile responsive design improvements
- [ ] Export session as PDF/PNG
- [ ] Detailed analytics and insights
- [ ] Drink ratings and reviews
- [ ] Bartender mode (professional recommendations)
- [ ] Cocktail recipe instructions
- [ ] Ingredient-based search
- [ ] Dietary restrictions and preferences

### Technical Improvements
- [ ] Add comprehensive test suite
- [ ] Implement CI/CD pipeline
- [ ] Add logging and monitoring
- [ ] Implement rate limiting
- [ ] Add Redis caching layer
- [ ] WebSocket support for real-time updates
- [ ] GraphQL API option
- [ ] Mobile app (React Native)

## Contributing Guidelines

### Code Style
- **Python**: Follow PEP 8, use Black formatter
- **TypeScript**: Use ESLint config, Prettier for formatting
- **Commits**: Use conventional commits format

### Pull Request Process
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes with clear commits
4. Update documentation
5. Test thoroughly
6. Submit PR with description

### Development Principles
- Keep it simple (KISS)
- Don't repeat yourself (DRY)
- Write self-documenting code
- Test before deploying
- Security first

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Vercel Docs](https://vercel.com/docs)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [TablePlus](https://tableplus.com/) - Database GUI
- [React DevTools](https://react.dev/learn/react-developer-tools)

## License

MIT License - Feel free to use for learning or building your own drink pairing app!

## Support

For issues, questions, or contributions:
- GitHub Issues: Create an issue in the repository
- Documentation: Check README.md and DEPLOYMENT.md
- API Docs: Visit `/docs` endpoint on backend

---

**Built with ❤️ using Claude AI** 🍹
