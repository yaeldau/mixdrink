# MixDrink - Quick Start Guide 🚀

Get MixDrink running in 5 minutes!

## Prerequisites Checklist

Make sure you have:
- ✅ Node.js 18+ installed (`node --version`)
- ✅ Python 3.11+ installed (`python --version`)
- ✅ Docker installed and running (`docker --version`)
- ✅ Anthropic API key ([Get one here](https://console.anthropic.com/))

## Setup Steps

### 1. Start the Database (30 seconds)

```bash
# From the mixdrink directory
docker-compose up -d

# Verify it's running
docker ps
# You should see: mixdrink_db running on port 5432
```

### 2. Start the Backend (2 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and paste your ANTHROPIC_API_KEY

# Run migrations and seed data
alembic upgrade head
python seed.py

# Start backend
uvicorn app.main:app --reload
```

**Backend running at:** http://localhost:8000
**API docs:** http://localhost:8000/docs

### 3. Start the Frontend (2 minutes)

Open a **new terminal** window:

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start frontend
npm run dev
```

**Frontend running at:** http://localhost:5173

## Verify Everything Works

1. Open http://localhost:5173 in your browser
2. You should see the MixDrink interface with:
   - Drink library on the left (50+ drinks)
   - Empty canvas in the center
   - Header with session controls

3. Try the app:
   - Search for "whiskey" in the search bar
   - Click "Add to Session" on "Old Fashioned"
   - Watch it appear in the ReactFlow diagram
   - Click "Get AI Recommendations" in the header
   - View Claude's suggestions in the right panel

## Troubleshooting

### Database Connection Error
```bash
# Make sure Docker is running
docker-compose down
docker-compose up -d
```

### Backend: Module not found
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Frontend: Port already in use
```bash
# Kill the process on port 5173
lsof -ti:5173 | xargs kill -9
npm run dev
```

### No drinks appearing
```bash
# Re-seed the database
cd backend
python seed.py
```

### AI recommendations not working
- Check your `.env` file has `ANTHROPIC_API_KEY=sk-...`
- Verify API key is valid at https://console.anthropic.com/

## Quick Commands

### Backend
```bash
# Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Reset database
alembic downgrade base && alembic upgrade head && python seed.py
```

### Frontend
```bash
# Start frontend
cd frontend && npm run dev

# Build for production
npm run build
```

### Docker
```bash
# Start database
docker-compose up -d

# Stop database
docker-compose down

# View logs
docker-compose logs -f
```

## What's Next?

Once everything is running:

1. **Explore the drink library** - Browse 50+ drinks with search and filters
2. **Build a session** - Add drinks and watch your journey visualize
3. **Get AI recommendations** - Let Claude suggest your next drink
4. **Track your session** - View stats on duration, drink count, and ABV

**Have fun and drink responsibly! 🥂**

---

**Need help?** Check the main [README.md](./README.md) for detailed documentation.
