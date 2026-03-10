import { create } from 'zustand';
import type {
  DrinkSession,
  ConsumedDrink,
  Recommendation,
  RecommendationResponse
} from '../types';
import { sessionApi, recommendationApi } from '../services/api';

interface SessionState {
  // State
  currentSession: DrinkSession | null;
  consumedDrinks: ConsumedDrink[];
  recommendations: Recommendation[];
  sessionContext: RecommendationResponse['session_context'] | null;
  isLoading: boolean;
  isLoadingRecommendations: boolean;
  error: string | null;

  // Actions
  loadCurrentSession: () => Promise<void>;
  consumeDrink: (drinkId: number, notes?: string) => Promise<void>;
  getRecommendations: () => Promise<void>;
  resetSession: () => Promise<void>;
  clearError: () => void;
}

export const useSessionStore = create<SessionState>((set, get) => ({
  // Initial state
  currentSession: null,
  consumedDrinks: [],
  recommendations: [],
  sessionContext: null,
  isLoading: false,
  isLoadingRecommendations: false,
  error: null,

  // Load current active session
  loadCurrentSession: async () => {
    set({ isLoading: true, error: null });
    try {
      const sessionData = await sessionApi.getCurrentSession();
      const { consumed_drinks, ...session } = sessionData;
      set({
        currentSession: session,
        consumedDrinks: consumed_drinks || [],
        isLoading: false
      });
    } catch (error: any) {
      // If no active session exists, that's okay - it will be created on first consume
      if (error?.response?.status === 404) {
        set({
          currentSession: null,
          consumedDrinks: [],
          isLoading: false
        });
      } else {
        const errorMessage = error instanceof Error ? error.message : 'Failed to load session';
        set({ error: errorMessage, isLoading: false });
        console.error('Error loading session:', error);
      }
    }
  },

  // Consume a drink in the current session
  consumeDrink: async (drinkId: number, notes?: string) => {
    set({ isLoading: true, error: null });
    try {
      await sessionApi.consumeDrink({
        drink_id: drinkId,
        notes
      });

      // Refresh the current session to get updated data
      await get().loadCurrentSession();

      set({ isLoading: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to consume drink';
      set({ error: errorMessage, isLoading: false });
      console.error('Error consuming drink:', error);
    }
  },

  // Get AI recommendations based on current session
  getRecommendations: async () => {
    set({ isLoadingRecommendations: true, error: null });
    try {
      const response = await recommendationApi.getRecommendations();
      set({
        recommendations: response.recommendations,
        sessionContext: response.session_context,
        isLoadingRecommendations: false
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to get recommendations';
      set({ error: errorMessage, isLoadingRecommendations: false });
      console.error('Error getting recommendations:', error);
    }
  },

  // Reset session (end current, start new)
  resetSession: async () => {
    set({ isLoading: true, error: null });
    try {
      const newSession = await sessionApi.resetSession();
      set({
        currentSession: newSession,
        consumedDrinks: [],
        recommendations: [],
        sessionContext: null,
        isLoading: false
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to reset session';
      set({ error: errorMessage, isLoading: false });
      console.error('Error resetting session:', error);
    }
  },

  // Clear error state
  clearError: () => {
    set({ error: null });
  },
}));
