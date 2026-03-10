import type { Drink } from '../types';

interface DrinkCardProps {
  drink: Drink;
  onConsume: (drinkId: number) => void;
  isConsuming?: boolean;
}

export function DrinkCard({ drink, onConsume, isConsuming = false }: DrinkCardProps) {
  const getCategoryColor = (category: string): string => {
    const colors: Record<string, string> = {
      spirit: 'bg-amber-100 text-amber-800 border-amber-300',
      cocktail: 'bg-purple-100 text-purple-800 border-purple-300',
      wine: 'bg-rose-100 text-rose-800 border-rose-300',
      beer: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      liqueur: 'bg-pink-100 text-pink-800 border-pink-300',
    };
    return colors[category.toLowerCase()] || 'bg-gray-100 text-gray-800 border-gray-300';
  };

  const renderFlavorProfile = () => {
    const flavors = drink.flavor_profile;
    const flavorNames: (keyof typeof flavors)[] = ['sweet', 'bitter', 'sour', 'savory', 'fruity'];

    return (
      <div className="space-y-1">
        {flavorNames.map((flavor) => {
          const value = flavors[flavor];
          if (value === 0) return null;

          return (
            <div key={flavor} className="flex items-center gap-2 text-xs">
              <span className="w-12 capitalize text-foreground/60">{flavor}</span>
              <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-400 to-blue-600 rounded-full transition-all"
                  style={{ width: `${(value / 5) * 100}%` }}
                />
              </div>
              <span className="w-8 text-right text-foreground/50">{value}/5</span>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="group relative bg-white border border-border rounded-lg p-4 hover:shadow-lg transition-shadow">
      {/* Category Badge */}
      <div className="flex items-center justify-between mb-3">
        <span className={`text-xs px-2 py-1 rounded-full border ${getCategoryColor(drink.category)}`}>
          {drink.category}
        </span>
        <span className="text-xs font-semibold text-foreground/70">
          {drink.alcohol_content}% ABV
        </span>
      </div>

      {/* Drink Name */}
      <h3 className="font-semibold text-lg mb-1 text-foreground">{drink.name}</h3>

      {/* Subcategory */}
      <p className="text-sm text-foreground/60 mb-2 capitalize">{drink.subcategory}</p>

      {/* Base Spirit (for cocktails) */}
      {drink.base_spirit && (
        <p className="text-xs text-foreground/50 mb-2">
          Base: <span className="capitalize">{drink.base_spirit}</span>
        </p>
      )}

      {/* Flavor Profile */}
      <div className="mb-4">
        {renderFlavorProfile()}
      </div>

      {/* Description (tooltip on hover) */}
      {drink.description && (
        <div className="mb-3">
          <p className="text-xs text-foreground/70 line-clamp-2 group-hover:line-clamp-none transition-all">
            {drink.description}
          </p>
        </div>
      )}

      {/* Ingredients (if available) */}
      {drink.ingredients && drink.ingredients.length > 0 && (
        <div className="mb-3">
          <p className="text-xs font-medium text-foreground/60 mb-1">Ingredients:</p>
          <div className="flex flex-wrap gap-1">
            {drink.ingredients.slice(0, 4).map((ingredient, idx) => (
              <span
                key={idx}
                className="text-xs px-2 py-0.5 bg-gray-100 text-gray-700 rounded-full"
              >
                {ingredient}
              </span>
            ))}
            {drink.ingredients.length > 4 && (
              <span className="text-xs px-2 py-0.5 text-gray-500">
                +{drink.ingredients.length - 4} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Add to Session Button */}
      <button
        onClick={() => onConsume(drink.id)}
        disabled={isConsuming}
        className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-md transition-colors text-sm font-medium"
      >
        {isConsuming ? 'Adding...' : 'Add to Session'}
      </button>
    </div>
  );
}
