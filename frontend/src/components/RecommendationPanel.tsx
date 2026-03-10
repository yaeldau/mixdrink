import { useSessionStore } from '../stores/sessionStore';
import { useDrinkStore } from '../stores/drinkStore';
import { Sparkles, Loader2, AlertCircle } from 'lucide-react';
import { useState } from 'react';

export function RecommendationPanel() {
  const {
    recommendations,
    sessionContext,
    consumedDrinks,
    consumeDrink,
    getRecommendations,
    isLoadingRecommendations,
    error,
  } = useSessionStore();

  const { drinks } = useDrinkStore();
  const [isConsuming, setIsConsuming] = useState(false);

  const hasRecommendations = recommendations.length > 0;
  const hasDrinks = consumedDrinks.length > 0;

  const handleConsumeDrink = async (drinkName: string) => {
    // Find the drink ID by name
    const drink = drinks.find(d => d.name.toLowerCase() === drinkName.toLowerCase());

    if (!drink) {
      console.error('Drink not found:', drinkName);
      alert(`Drink "${drinkName}" not found in the catalog.`);
      return;
    }

    setIsConsuming(true);
    try {
      await consumeDrink(drink.id);
      // Optionally refresh recommendations after consuming
      // await getRecommendations();
    } catch (error) {
      console.error('Error consuming drink:', error);
    } finally {
      setIsConsuming(false);
    }
  };

  // Don't show panel if no drinks consumed yet
  if (!hasDrinks) {
    return null;
  }

  return (
    <div className="flex flex-col h-full bg-white border-l border-border">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-blue-600" />
            AI Recommendations
          </h2>
        </div>
        <p className="text-xs text-foreground/60">
          Claude AI suggests your next drink based on your session
        </p>
      </div>

      {/* Error State */}
      {error && (
        <div className="m-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
          <AlertCircle className="w-4 h-4 text-red-600 mt-0.5 flex-shrink-0" />
          <div className="flex-1">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoadingRecommendations && (
        <div className="flex-1 flex flex-col items-center justify-center p-4">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600 mb-3" />
          <p className="text-sm text-foreground/60">Getting recommendations...</p>
        </div>
      )}

      {/* Empty State (no recommendations yet) */}
      {!isLoadingRecommendations && !hasRecommendations && !error && (
        <div className="flex-1 flex flex-col items-center justify-center p-4 text-center">
          <Sparkles className="w-12 h-12 text-gray-400 mb-3" />
          <p className="text-sm text-foreground/60 mb-2">
            Click "Get AI Recommendations" to see suggestions
          </p>
          <p className="text-xs text-foreground/40">
            Based on your {consumedDrinks.length} consumed {consumedDrinks.length === 1 ? 'drink' : 'drinks'}
          </p>
        </div>
      )}

      {/* Recommendations List */}
      {!isLoadingRecommendations && hasRecommendations && (
        <div className="flex-1 overflow-y-auto p-4">
          {/* Session Context */}
          {sessionContext && (
            <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <h3 className="text-xs font-semibold text-blue-900 mb-2">Session Summary</h3>
              <div className="space-y-1 text-xs text-blue-800">
                <div className="flex justify-between">
                  <span>Drinks consumed:</span>
                  <span className="font-semibold">{sessionContext.drinks_consumed}</span>
                </div>
                <div className="flex justify-between">
                  <span>Total alcohol:</span>
                  <span className="font-semibold">{sessionContext.total_alcohol.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span>Duration:</span>
                  <span className="font-semibold">{sessionContext.session_duration_minutes} min</span>
                </div>
              </div>
            </div>
          )}

          {/* Recommendations */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-foreground mb-2">
              Suggested Next Drinks:
            </h3>
            {recommendations.map((rec, index) => (
              <div
                key={index}
                className="p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all"
              >
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-semibold text-sm text-foreground">{rec.drink_name}</h4>
                  <span className="text-xs px-2 py-0.5 bg-blue-100 text-blue-800 rounded-full">
                    #{index + 1}
                  </span>
                </div>
                <p className="text-xs text-foreground/70 mb-3 leading-relaxed">
                  {rec.reasoning}
                </p>
                <button
                  onClick={() => handleConsumeDrink(rec.drink_name)}
                  disabled={isConsuming}
                  className="w-full py-2 px-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-md transition-colors text-xs font-medium"
                >
                  {isConsuming ? 'Adding...' : 'Add to Session'}
                </button>
              </div>
            ))}
          </div>

          {/* Refresh Button */}
          <button
            onClick={() => getRecommendations()}
            disabled={isLoadingRecommendations}
            className="w-full mt-4 py-2 px-4 border border-gray-300 hover:bg-gray-50 disabled:bg-gray-100 text-gray-700 rounded-lg transition-colors text-sm font-medium"
          >
            Refresh Recommendations
          </button>
        </div>
      )}
    </div>
  );
}
