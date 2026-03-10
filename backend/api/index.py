import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.main import app

# Export FastAPI app directly - Vercel will handle ASGI
app = app
