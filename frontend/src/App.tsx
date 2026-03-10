import { useEffect } from 'react';
import { useSessionStore } from './stores/sessionStore';
import { DrinkLibrary } from './components/DrinkLibrary';
import { DrinkFlowDiagram } from './components/DrinkFlowDiagram';
import { RecommendationPanel } from './components/RecommendationPanel';
import { SessionControls } from './components/SessionControls';
import { Wine } from 'lucide-react';

function App() {
  const { loadCurrentSession, consumedDrinks } = useSessionStore();

  // Load current session on mount
  useEffect(() => {
    loadCurrentSession();
  }, [loadCurrentSession]);

  const hasDrinks = consumedDrinks.length > 0;

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-border shadow-sm">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo and Title */}
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2 rounded-lg">
                <Wine className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">MixDrink</h1>
                <p className="text-sm text-foreground/60">AI-Powered Drink Pairing Assistant</p>
              </div>
            </div>

            {/* Session Controls */}
            <SessionControls />
          </div>
        </div>
      </header>

      {/* Main Layout */}
      <main className="flex-1 flex overflow-hidden">
        {/* Left Sidebar - Drink Library */}
        <aside className="w-96 bg-white border-r border-border overflow-hidden flex flex-col">
          <DrinkLibrary />
        </aside>

        {/* Center - ReactFlow Diagram */}
        <section className="flex-1 overflow-hidden">
          <DrinkFlowDiagram />
        </section>

        {/* Right Sidebar - Recommendation Panel (conditional) */}
        {hasDrinks && (
          <aside className="w-96 overflow-hidden flex flex-col">
            <RecommendationPanel />
          </aside>
        )}
      </main>
    </div>
  );
}

export default App;
