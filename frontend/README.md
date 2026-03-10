# MixDrink Frontend

React + TypeScript frontend for the MixDrink AI-powered drink pairing application.

## Tech Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Zustand** - State management
- **ReactFlow** - Interactive flow diagrams
- **Tailwind CSS** - Styling
- **Axios** - API client

## Project Structure

```
src/
├── components/       # React components
├── stores/          # Zustand state stores
├── services/        # API clients and utilities
├── types/           # TypeScript type definitions
├── App.tsx          # Main application component
├── main.tsx         # Application entry point
└── index.css        # Global styles and Tailwind imports
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

### Installation

```bash
npm install
```

### Development

```bash
# Start dev server (http://localhost:5173)
npm run dev
```

### Build

```bash
# Production build
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```
VITE_API_URL=http://localhost:8000
```

## Architecture

### State Management

The app uses Zustand for state management with two main stores:

- **drinkStore** - Manages drink catalog, search, and filters
- **sessionStore** - Manages active session, consumed drinks, and AI recommendations

### API Integration

All backend communication is centralized in `src/services/api.ts`:

- `drinkApi` - Drink catalog endpoints
- `sessionApi` - Session management endpoints
- `recommendationApi` - AI recommendation endpoints

### Components

Key components:

- **DrinkLibrary** - Browse and search drinks
- **DrinkCard** - Individual drink display
- **DrinkFlowDiagram** - ReactFlow visualization of consumption journey
- **RecommendationPanel** - Display AI-generated suggestions
- **SessionControls** - Session management controls

## Development Status

✅ Infrastructure setup complete
⏳ Stores implementation pending
⏳ Component implementation pending
⏳ Integration pending
