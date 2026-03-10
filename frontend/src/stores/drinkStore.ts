import { create } from 'zustand';
import type { Drink, DrinkFilters } from '../types';
import { drinkApi } from '../services/api';

interface DrinkState {
  // State
  drinks: Drink[];
  isLoading: boolean;
  error: string | null;
  searchQuery: string;
  selectedCategory: string | null;
  selectedSubcategory: string | null;

  // Actions
  fetchDrinks: () => Promise<void>;
  searchDrinks: (query: string) => Promise<void>;
  filterByCategory: (category: string | null) => Promise<void>;
  filterBySubcategory: (subcategory: string | null) => Promise<void>;
  clearFilters: () => Promise<void>;
  setSearchQuery: (query: string) => void;
}

export const useDrinkStore = create<DrinkState>((set, get) => ({
  // Initial state
  drinks: [],
  isLoading: false,
  error: null,
  searchQuery: '',
  selectedCategory: null,
  selectedSubcategory: null,

  // Fetch all drinks with current filters
  fetchDrinks: async () => {
    set({ isLoading: true, error: null });
    try {
      const filters: DrinkFilters = {
        search: get().searchQuery || undefined,
        category: get().selectedCategory || undefined,
        subcategory: get().selectedSubcategory || undefined,
      };

      const drinks = await drinkApi.getDrinks(filters);
      set({ drinks, isLoading: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to fetch drinks';
      set({ error: errorMessage, isLoading: false });
      console.error('Error fetching drinks:', error);
    }
  },

  // Search drinks by query
  searchDrinks: async (query: string) => {
    set({ searchQuery: query, isLoading: true, error: null });
    try {
      const filters: DrinkFilters = {
        search: query || undefined,
        category: get().selectedCategory || undefined,
        subcategory: get().selectedSubcategory || undefined,
      };

      const drinks = await drinkApi.getDrinks(filters);
      set({ drinks, isLoading: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to search drinks';
      set({ error: errorMessage, isLoading: false });
      console.error('Error searching drinks:', error);
    }
  },

  // Filter by category
  filterByCategory: async (category: string | null) => {
    set({ selectedCategory: category, selectedSubcategory: null, isLoading: true, error: null });
    try {
      const filters: DrinkFilters = {
        search: get().searchQuery || undefined,
        category: category || undefined,
      };

      const drinks = await drinkApi.getDrinks(filters);
      set({ drinks, isLoading: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to filter drinks';
      set({ error: errorMessage, isLoading: false });
      console.error('Error filtering drinks:', error);
    }
  },

  // Filter by subcategory
  filterBySubcategory: async (subcategory: string | null) => {
    set({ selectedSubcategory: subcategory, isLoading: true, error: null });
    try {
      const filters: DrinkFilters = {
        search: get().searchQuery || undefined,
        category: get().selectedCategory || undefined,
        subcategory: subcategory || undefined,
      };

      const drinks = await drinkApi.getDrinks(filters);
      set({ drinks, isLoading: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to filter drinks';
      set({ error: errorMessage, isLoading: false });
      console.error('Error filtering drinks:', error);
    }
  },

  // Clear all filters
  clearFilters: async () => {
    set({
      searchQuery: '',
      selectedCategory: null,
      selectedSubcategory: null,
      isLoading: true,
      error: null
    });
    try {
      const drinks = await drinkApi.getDrinks({});
      set({ drinks, isLoading: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to fetch drinks';
      set({ error: errorMessage, isLoading: false });
      console.error('Error fetching drinks:', error);
    }
  },

  // Set search query without fetching (for controlled input)
  setSearchQuery: (query: string) => {
    set({ searchQuery: query });
  },
}));
