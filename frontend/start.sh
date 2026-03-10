#!/bin/bash

# Start MixDrink Frontend Development Server

echo "🍸 Starting MixDrink Frontend..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
fi

echo "🚀 Starting development server..."
echo "Frontend will be available at: http://localhost:5173"
echo ""

npm run dev
