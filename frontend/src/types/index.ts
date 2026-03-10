// Core data models for MixDrink application

export interface FlavorProfile {
  sweet: number; // 1-5
  bitter: number; // 1-5
  sour: number; // 1-5
  savory: number; // 1-5
  fruity: number; // 1-5
}

export interface Drink {
  id: number;
  name: string;
  category: string; // spirit, cocktail, wine, beer, liqueur
  subcategory: string; // vodka, whiskey, IPA, red_wine, etc.
  alcohol_content: number; // ABV %
  flavor_profile: FlavorProfile;
  description: string;
  base_spirit?: string; // for cocktails
  ingredients?: string[]; // array of ingredient names
  image_url?: string;
}

export interface DrinkSession {
  id: number;
  session_name?: string;
  started_at: string; // ISO timestamp
  ended_at?: string; // ISO timestamp, nullable
  is_active: boolean;
}

export interface ConsumedDrink {
  id: number;
  session_id: number;
  drink_id: number;
  consumed_at: string; // ISO timestamp
  drink_order: number; // 1st, 2nd, 3rd drink...
  notes?: string;
  drink?: Drink; // populated by backend
}

export interface SessionWithDrinks {
  session: DrinkSession;
  consumed_drinks: ConsumedDrink[];
}

export interface Recommendation {
  drink_name: string;
  reasoning: string;
}

export interface RecommendationResponse {
  recommendations: Recommendation[];
  session_context: {
    drinks_consumed: number;
    total_alcohol: number;
    session_duration_minutes: number;
  };
}

// API request/response types
export interface ConsumeDrinkRequest {
  drink_id: number;
  notes?: string;
}

export interface DrinkFilters {
  search?: string;
  category?: string;
  subcategory?: string;
}
