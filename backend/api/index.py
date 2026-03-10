# Vercel serverless function entry point
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.main import app

# Export app as handler for Vercel
handler = app
