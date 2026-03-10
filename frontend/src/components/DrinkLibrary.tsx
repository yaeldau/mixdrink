import { useEffect } from 'react';
import { useDrinkStore } from '../stores/drinkStore';
import { useSessionStore } from '../stores/sessionStore';
import { DrinkCard } from './DrinkCard';
import { SearchBar } from './SearchBar';
import { Loader2 } from 'lucide-react';

const CATEGORIES = [
  { value: 'all', label: 'All Drinks' },
  { value: 'spirit', label: 'Spirits' },
  { value: 'cocktail', label: 'Cocktails' },
  { value: 'wine', label: 'Wine' },
  { value: 'beer', label: 'Beer' },
  { value: 'liqueur', label: 'Liqueurs' },
];

export function DrinkLibrary() {
  const {
    drinks,
    isLoading,
    error,
    searchQuery,
    selectedCategory,
    fetchDrinks,
    searchDrinks,
    filterByCategory,
    setSearchQuery,
  } = useDrinkStore();

  const {
    consumeDrink,
    isLoading: isConsumingDrink,
  } = useSessionStore();

  // Load drinks on mount
  useEffect(() => {
    fetchDrinks();
  }, [fetchDrinks]);

  const handleCategoryClick = (category: string) => {
    if (category === 'all') {
      filterByCategory(null);
    } else {
      filterByCategory(category);
    }
  };

  const handleConsumeDrink = async (drinkId: number) => {
    try {
      await consumeDrink(drinkId);
    } catch (error) {
      console.error('Error consuming drink:', error);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-border bg-white">
        <h2 className="text-lg font-semibold mb-3 text-foreground">Drink Library</h2>

        {/* Search Bar */}
        <SearchBar
          value={searchQuery}
          onChange={setSearchQuery}
          onSearch={searchDrinks}
          placeholder="Search by name, spirit, or ingredient..."
        />

        {/* Category Filter Chips */}
        <div className="flex flex-wrap gap-2 mt-3">
          {CATEGORIES.map((category) => {
            const isActive = category.value === 'all'
              ? selectedCategory === null
              : selectedCategory === category.value;

            return (
              <button
                key={category.value}
                onClick={() => handleCategoryClick(category.value)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {category.label}
              </button>
            );
          })}
        </div>

        {/* Results Count */}
        {!isLoading && drinks.length > 0 && (
          <p className="text-xs text-foreground/60 mt-3">
            {drinks.length} {drinks.length === 1 ? 'drink' : 'drinks'} found
          </p>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="mx-4 mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        </div>
      )}

      {/* Empty State */}
      {!isLoading && drinks.length === 0 && !error && (
        <div className="flex flex-col items-center justify-center py-20 px-4">
          <p className="text-foreground/60 text-center mb-2">No drinks found</p>
          <p className="text-sm text-foreground/40 text-center">
            Try adjusting your search or filters
          </p>
        </div>
      )}

      {/* Drink Grid */}
      {!isLoading && drinks.length > 0 && (
        <div className="flex-1 overflow-y-auto p-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {drinks.map((drink) => (
              <DrinkCard
                key={drink.id}
                drink={drink}
                onConsume={handleConsumeDrink}
                isConsuming={isConsumingDrink}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
