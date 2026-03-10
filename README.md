# MixDrink 🍸

An AI-powered drink pairing application that helps you discover compatible drink combinations and track your drinking session with intelligent recommendations from Claude AI.

![MixDrink](https://img.shields.io/badge/Status-MVP-green) ![License](https://img.shields.io/badge/License-MIT-blue)

## Features

### 🔍 **Drink Library**
- Browse 50+ drinks (spirits, cocktails, wine, beer, liqueurs)
- Search by name, spirit, or ingredient
- Filter by category and subcategory
- Visual flavor profiles (sweet, bitter, sour, savory, fruity)
- Detailed drink information with ingredients

### 🎨 **Visual Session Tracking**
- Interactive ReactFlow diagram showing your drinking journey
- Horizontal timeline of consumed drinks
- Color-coded by category (spirits, cocktails, wine, beer, liqueurs)
- Session statistics (duration, drink count, average ABV)

### 🤖 **AI-Powered Recommendations**
- Claude AI suggests next drinks based on:
  - Flavor progression (build or contrast)
  - Alcohol pacing (avoid spiking ABV too quickly)
  - Palate cleansing (variety in base spirits)
  - Session context (time, drink count)
- Contextual reasoning for each suggestion
- One-click to add recommended drinks

### 📊 **Session Management**
- Auto-creates session on first drink
- Track time, drink count, and alcohol consumption
- Reset session anytime to start fresh
- Persistent session data (survives page refresh)

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLAlchemy** (async) - ORM
- **Anthropic Claude API** - AI recommendations
- **Alembic** - Database migrations
- **Docker** - Containerization

### Frontend
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Zustand** - State management
- **ReactFlow** - Interactive flow diagrams
- **Tailwind CSS** - Styling
- **Axios** - API client
- **Lucide React** - Icons

## Project Structure

```
mixdrink/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/   # API endpoints
│   │   ├── db/
│   │   │   ├── models.py # Database models
│   │   │   └── seed_data.py
│   │   ├── services/     # Business logic
│   │   └── models/       # Pydantic schemas
│   ├── alembic/          # Database migrations
│   ├── requirements.txt
│   └── .env.example
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── stores/       # Zustand stores
│   │   ├── services/     # API clients
│   │   └── types/        # TypeScript types
│   ├── package.json
│   └── .env.example
└── docker-compose.yml    # PostgreSQL setup
```

## Getting Started

### Prerequisites

- **Node.js 18+** and npm
- **Python 3.11+**
- **Docker** and Docker Compose
- **Anthropic API Key** ([Get one here](https://console.anthropic.com/))

### Installation

#### 1. Clone the repository

```bash
cd mixdrink
```

#### 2. Set up the database

```bash
# Start PostgreSQL with Docker
docker-compose up -d

# Verify database is running
docker ps
```

#### 3. Set up the backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run database migrations
alembic upgrade head

# Seed the database with drinks
python seed.py

# Start the backend server
uvicorn app.main:app --reload
```

Backend will be running at: **http://localhost:8000**

API docs available at: **http://localhost:8000/docs**

#### 4. Set up the frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
# Verify VITE_API_URL=http://localhost:8000

# Start the dev server
npm run dev
```

Frontend will be running at: **http://localhost:5173**

## Usage

### Basic Workflow

1. **Browse Drinks**: Use the left sidebar to search and filter drinks
2. **Add to Session**: Click "Add to Session" on any drink card
3. **View Journey**: See your consumption journey visualized in the center canvas
4. **Get Recommendations**: Click "Get AI Recommendations" in the header
5. **Explore Suggestions**: View Claude's reasoning and add suggested drinks
6. **Reset Session**: Clear your session anytime to start fresh

### Example Session

1. Start with a **Gin & Tonic** (refreshing, citrus)
2. Get AI recommendations → suggests **Aperol Spritz** (similar light profile)
3. Add Aperol Spritz
4. Get AI recommendations → suggests **Negroni** (bitter complexity)
5. View your flavor progression in the diagram

## API Endpoints

### Drinks
- `GET /api/drinks` - List all drinks with filters
- `GET /api/drinks/{id}` - Get drink details

### Session
- `POST /api/session/start` - Start new session
- `GET /api/session/current` - Get active session
- `POST /api/session/consume` - Add drink to session
- `DELETE /api/session/reset` - Reset session
- `GET /api/session/history` - Get past sessions

### Recommendations
- `POST /api/recommendations` - Get AI drink suggestions

## Database Schema

### Drink
```sql
id, name, category, subcategory, alcohol_content,
flavor_profile (JSON), description, base_spirit,
ingredients (JSON), image_url
```

### DrinkSession
```sql
id, session_name, started_at, ended_at, is_active
```

### ConsumedDrink
```sql
id, session_id, drink_id, consumed_at, drink_order, notes
```

## Development

### Backend Development

```bash
cd backend

# Run tests (when available)
pytest

# Create new migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Frontend Development

```bash
cd frontend

# Run linter
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

## Claude AI Integration

The app uses Claude AI (via Anthropic API) to generate intelligent drink recommendations based on:

- **Flavor progression**: Building complementary flavors or creating contrasts
- **Alcohol pacing**: Preventing rapid ABV increases
- **Palate cleansing**: Recommending variety in base spirits
- **Session context**: Considering time, drink count, and total alcohol

The prompt engineering includes:
- System prompt with expert mixologist persona
- User message with session history and flavor profiles
- Structured output with drink names and reasoning

## Future Enhancements

- [ ] User authentication and profiles
- [ ] Save and share session histories
- [ ] Custom drink creation
- [ ] Social features (share sessions with friends)
- [ ] Mobile responsive design
- [ ] Export diagram as PNG/PDF
- [ ] Detailed analytics and insights
- [ ] Drink rating and reviews
- [ ] Bartender mode (professional recommendations)

## Contributing

This is an MVP project. Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this project for learning or building your own drink pairing app!

## Acknowledgments

- **Anthropic Claude API** - AI-powered recommendations
- **ReactFlow** - Interactive diagram visualization
- **FastAPI** - Modern Python web framework
- **Tailwind CSS** - Beautiful, responsive styling

---

**Built with ❤️ and 🍸 by the MixDrink team**

Enjoy responsibly! 🥂
