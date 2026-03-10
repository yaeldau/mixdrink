import { useState, useEffect } from 'react';
import { Search, X, Loader2, RefreshCw, Wine, Sparkles } from 'lucide-react';

// Helper function to get drink icon
const getDrinkIcon = (drinkName: string) => {
  const name = drinkName.toLowerCase();
  if (name.includes('wine')) return '🍷';
  if (name.includes('champagne') || name.includes('sparkling')) return '🥂';
  if (name.includes('beer') || name.includes('ipa') || name.includes('lager') || name.includes('stout')) return '🍺';
  if (name.includes('vodka')) return '🥃';
  if (name.includes('whiskey') || name.includes('bourbon') || name.includes('scotch')) return '🥃';
  if (name.includes('gin')) return '🍸';
  if (name.includes('rum')) return '🍹';
  if (name.includes('tequila')) return '🍹';
  if (name.includes('cocktail')) return '🍸';
  if (name.includes('liqueur')) return '🥃';
  return '🥤';
};

interface Drink {
  id: number;
  name: string;
  category: string;
  subcategory?: string;
}

interface Recommendation {
  drink_name: string;
  explanation: string;
}

interface PairingResponse {
  good_combinations: Recommendation[];
  okay_combinations: Recommendation[];
  not_recommended: Recommendation[];
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function DrinkPairing() {
  const [allDrinks, setAllDrinks] = useState<Drink[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDrinks, setSelectedDrinks] = useState<string[]>([]);
  const [recommendations, setRecommendations] = useState<PairingResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);

  // Load all drinks on mount
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/drinks?limit=200`)
      .then(res => res.json())
      .then(data => setAllDrinks(data))
      .catch(err => console.error('Failed to load drinks:', err));
  }, []);

  // Filter drinks based on search query - match name, category, or subcategory
  const filteredDrinks = allDrinks.filter(drink => {
    if (selectedDrinks.includes(drink.name)) return false;

    const query = searchQuery.toLowerCase();
    const name = drink.name.toLowerCase();
    const category = drink.category.toLowerCase();
    const subcategory = (drink as any).subcategory?.toLowerCase() || '';

    // Match name, category, or subcategory (with or without underscore)
    return name.includes(query) ||
           category.includes(query) ||
           subcategory.includes(query) ||
           subcategory.replace('_', ' ').includes(query);
  });

  const addDrink = (drinkName: string) => {
    if (!selectedDrinks.includes(drinkName)) {
      setSelectedDrinks([...selectedDrinks, drinkName]);
      setSearchQuery('');
      setShowDropdown(false);
    }
  };

  const removeDrink = (drinkName: string) => {
    setSelectedDrinks(selectedDrinks.filter(d => d !== drinkName));
    setRecommendations(null);
  };

  const getRecommendations = async () => {
    if (selectedDrinks.length === 0) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/pairing/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ consumed_drinks: selectedDrinks })
      });
      const data = await response.json();
      setRecommendations(data);
    } catch (err) {
      console.error('Failed to get recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setSelectedDrinks([]);
    setRecommendations(null);
    setSearchQuery('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="max-w-2xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Wine className="w-12 h-12 text-purple-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            MixDrink
          </h1>
          <p className="text-gray-600">
            AI-powered drink pairing recommendations
          </p>
        </div>

        {/* Search Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            What have you been drinking?
          </label>
          <div className="relative">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setShowDropdown(true);
                }}
                onFocus={() => setShowDropdown(true)}
                placeholder="Search for drinks (e.g., whiskey, red wine, rum)..."
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none text-base"
              />
            </div>

            {/* Dropdown */}
            {showDropdown && searchQuery && (
              <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                {filteredDrinks.length > 0 ? (
                  filteredDrinks.slice(0, 15).map((drink) => {
                    const subcategoryDisplay = drink.subcategory
                      ? drink.subcategory.replace('_', ' ')
                      : drink.category;

                    return (
                      <button
                        key={drink.id}
                        onClick={() => addDrink(drink.name)}
                        className="w-full px-4 py-3 text-left hover:bg-purple-50 transition-colors border-b border-gray-100 last:border-b-0"
                      >
                        <div className="font-medium text-gray-900">{drink.name}</div>
                        <div className="text-xs text-gray-500 capitalize">{subcategoryDisplay}</div>
                      </button>
                    );
                  })
                ) : (
                  <div className="px-4 py-3 text-sm text-gray-500">
                    No drinks found. Try searching for specific names like "Merlot", "Whiskey", or "Vodka"
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Selected Drinks */}
        {selectedDrinks.length > 0 && (
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Selected drinks:
            </label>
            <div className="flex flex-wrap gap-2">
              {selectedDrinks.map((drink) => (
                <div
                  key={drink}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-purple-100 text-purple-800 rounded-full text-sm font-medium"
                >
                  {drink}
                  <button
                    onClick={() => removeDrink(drink)}
                    className="hover:bg-purple-200 rounded-full p-1 transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Get Recommendations Button */}
        {selectedDrinks.length > 0 && !recommendations && (
          <button
            onClick={getRecommendations}
            disabled={loading}
            className="w-full py-5 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold rounded-xl transition-all flex items-center justify-center gap-3 text-lg shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98]"
          >
            {loading ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                Analyzing your drinks...
              </>
            ) : (
              <>
                <Sparkles className="w-6 h-6" />
                Get Smart Recommendations
              </>
            )}
          </button>
        )}

        {/* Recommendations */}
        {recommendations && (
          <div className="space-y-6 mb-6">
            {/* Context Header */}
            <div className="bg-gradient-to-r from-purple-100 to-blue-100 border border-purple-200 rounded-xl p-4">
              <h2 className="text-sm font-semibold text-purple-900 mb-2">
                Based on what you've had:
              </h2>
              <div className="flex flex-wrap gap-2">
                {selectedDrinks.map((drink) => (
                  <span
                    key={drink}
                    className="px-3 py-1 bg-white text-purple-800 rounded-full text-sm font-medium shadow-sm"
                  >
                    {drink}
                  </span>
                ))}
              </div>
            </div>

            {/* Good Combinations */}
            <RecommendationSection
              title="✨ Great Next Choices"
              subtitle="These drinks will complement your taste progression"
              recommendations={recommendations.good_combinations}
              color="green"
              emoji="🎯"
            />

            {/* Okay Combinations */}
            <RecommendationSection
              title="👌 Safe Alternatives"
              subtitle="Won't clash, but not the most exciting pairings"
              recommendations={recommendations.okay_combinations}
              color="yellow"
              emoji="⚖️"
            />

            {/* Not Recommended */}
            <RecommendationSection
              title="⚠️ Better to Avoid"
              subtitle="These might clash or cause flavor fatigue"
              recommendations={recommendations.not_recommended}
              color="red"
              emoji="🚫"
            />
          </div>
        )}

        {/* Reset Button */}
        {(selectedDrinks.length > 0 || recommendations) && (
          <button
            onClick={reset}
            className="w-full py-4 bg-white border-2 border-gray-300 hover:border-gray-400 hover:bg-gray-50 text-gray-700 font-semibold rounded-xl transition-all flex items-center justify-center gap-2 shadow-sm hover:shadow"
          >
            <RefreshCw className="w-5 h-5" />
            Clear & Start Over
          </button>
        )}
      </div>
    </div>
  );
}

interface RecommendationSectionProps {
  title: string;
  subtitle: string;
  recommendations: Recommendation[];
  color: 'green' | 'yellow' | 'red';
  emoji: string;
}

function RecommendationSection({ title, subtitle, recommendations, color, emoji }: RecommendationSectionProps) {
  const colorClasses = {
    green: {
      border: 'border-green-300',
      bg: 'bg-gradient-to-br from-green-50 to-emerald-50',
      title: 'text-green-900',
      subtitle: 'text-green-700',
      card: 'bg-white border-green-200 hover:border-green-300',
      badge: 'bg-green-500'
    },
    yellow: {
      border: 'border-amber-300',
      bg: 'bg-gradient-to-br from-amber-50 to-yellow-50',
      title: 'text-amber-900',
      subtitle: 'text-amber-700',
      card: 'bg-white border-amber-200 hover:border-amber-300',
      badge: 'bg-amber-500'
    },
    red: {
      border: 'border-red-300',
      bg: 'bg-gradient-to-br from-red-50 to-rose-50',
      title: 'text-red-900',
      subtitle: 'text-red-700',
      card: 'bg-white border-red-200 hover:border-red-300',
      badge: 'bg-red-500'
    }
  };

  const styles = colorClasses[color];

  return (
    <div className={`border-2 ${styles.border} ${styles.bg} rounded-2xl p-5 shadow-sm`}>
      <div className="flex items-start gap-3 mb-4">
        <div className="text-3xl">{emoji}</div>
        <div className="flex-1">
          <h2 className={`text-xl font-bold ${styles.title} mb-1`}>{title}</h2>
          <p className={`text-sm ${styles.subtitle}`}>{subtitle}</p>
        </div>
      </div>

      <div className="space-y-3">
        {recommendations.map((rec, idx) => (
          <div
            key={idx}
            className={`${styles.card} border-2 rounded-xl p-4 shadow-sm transition-all hover:shadow-md relative overflow-hidden`}
          >
            {/* Badge */}
            <div className={`absolute top-0 right-0 w-1 h-full ${styles.badge}`}></div>

            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 text-3xl">
                {getDrinkIcon(rec.drink_name)}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h3 className="font-bold text-gray-900 text-lg">{rec.drink_name}</h3>
                  <span className="text-xs font-semibold px-2 py-1 rounded-full bg-gray-100 text-gray-600">
                    #{idx + 1}
                  </span>
                </div>
                <p className="text-sm text-gray-600 leading-relaxed">{rec.explanation}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
