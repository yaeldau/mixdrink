import React, { useState, useEffect } from 'react';
import { Search, X, Loader2, RefreshCw, Wine } from 'lucide-react';

interface Drink {
  id: number;
  name: string;
  category: string;
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

  // Filter drinks based on search query
  const filteredDrinks = allDrinks.filter(drink =>
    drink.name.toLowerCase().includes(searchQuery.toLowerCase()) &&
    !selectedDrinks.includes(drink.name)
  );

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
            {showDropdown && searchQuery && filteredDrinks.length > 0 && (
              <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                {filteredDrinks.slice(0, 10).map((drink) => (
                  <button
                    key={drink.id}
                    onClick={() => addDrink(drink.name)}
                    className="w-full px-4 py-3 text-left hover:bg-purple-50 transition-colors border-b border-gray-100 last:border-b-0"
                  >
                    <div className="font-medium text-gray-900">{drink.name}</div>
                    <div className="text-xs text-gray-500 capitalize">{drink.category}</div>
                  </button>
                ))}
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
            className="w-full py-4 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors flex items-center justify-center gap-2 text-lg shadow-md"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Getting recommendations...
              </>
            ) : (
              'Get Pairing Recommendations'
            )}
          </button>
        )}

        {/* Recommendations */}
        {recommendations && (
          <div className="space-y-6 mb-6">
            {/* Good Combinations */}
            <RecommendationSection
              title="✨ Great Combinations"
              subtitle="Excellent pairings that complement what you've had"
              recommendations={recommendations.good_combinations}
              color="green"
            />

            {/* Okay Combinations */}
            <RecommendationSection
              title="👍 Okay Combinations"
              subtitle="Acceptable pairings that won't clash"
              recommendations={recommendations.okay_combinations}
              color="yellow"
            />

            {/* Not Recommended */}
            <RecommendationSection
              title="⚠️ Not Recommended"
              subtitle="Combinations to avoid"
              recommendations={recommendations.not_recommended}
              color="red"
            />
          </div>
        )}

        {/* Reset Button */}
        {(selectedDrinks.length > 0 || recommendations) && (
          <button
            onClick={reset}
            className="w-full py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Start Over
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
}

function RecommendationSection({ title, subtitle, recommendations, color }: RecommendationSectionProps) {
  const colorClasses = {
    green: {
      border: 'border-green-200',
      bg: 'bg-green-50',
      title: 'text-green-900',
      subtitle: 'text-green-700',
      card: 'bg-white border-green-100'
    },
    yellow: {
      border: 'border-yellow-200',
      bg: 'bg-yellow-50',
      title: 'text-yellow-900',
      subtitle: 'text-yellow-700',
      card: 'bg-white border-yellow-100'
    },
    red: {
      border: 'border-red-200',
      bg: 'bg-red-50',
      title: 'text-red-900',
      subtitle: 'text-red-700',
      card: 'bg-white border-red-100'
    }
  };

  const styles = colorClasses[color];

  return (
    <div className={`border-2 ${styles.border} ${styles.bg} rounded-xl p-4`}>
      <h2 className={`text-xl font-bold ${styles.title} mb-1`}>{title}</h2>
      <p className={`text-sm ${styles.subtitle} mb-4`}>{subtitle}</p>

      <div className="space-y-3">
        {recommendations.map((rec, idx) => (
          <div
            key={idx}
            className={`${styles.card} border rounded-lg p-4 shadow-sm`}
          >
            <h3 className="font-semibold text-gray-900 mb-1">{rec.drink_name}</h3>
            <p className="text-sm text-gray-600">{rec.explanation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
