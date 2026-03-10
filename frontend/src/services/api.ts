import axios from 'axios';
import type {
  Drink,
  DrinkFilters,
  SessionWithDrinks,
  ConsumeDrinkRequest,
  ConsumedDrink,
  RecommendationResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log('API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      message: error.message,
      data: error.response?.data,
    });
    return Promise.reject(error);
  }
);

// Drink catalog API
export const drinkApi = {
  // Get all drinks with optional filters
  getDrinks: async (filters?: DrinkFilters): Promise<Drink[]> => {
    const params = new URLSearchParams();
    if (filters?.search) params.append('search', filters.search);
    if (filters?.category) params.append('category', filters.category);
    if (filters?.subcategory) params.append('subcategory', filters.subcategory);

    const response = await api.get<Drink[]>(`/api/drinks?${params.toString()}`);
    return response.data;
  },

  // Get single drink by ID
  getDrink: async (id: number): Promise<Drink> => {
    const response = await api.get<Drink>(`/api/drinks/${id}`);
    return response.data;
  },
};

// Session management API
export const sessionApi = {
  // Start a new session
  startSession: async (): Promise<SessionWithDrinks> => {
    const response = await api.post<SessionWithDrinks>('/api/session/start');
    return response.data;
  },

  // Get current active session
  getCurrentSession: async (): Promise<SessionWithDrinks> => {
    const response = await api.get<SessionWithDrinks>('/api/session/current');
    return response.data;
  },

  // Consume a drink in the current session
  consumeDrink: async (data: ConsumeDrinkRequest): Promise<ConsumedDrink> => {
    const response = await api.post<ConsumedDrink>('/api/session/consume', data);
    return response.data;
  },

  // Reset session (end current, start new)
  resetSession: async (): Promise<SessionWithDrinks> => {
    const response = await api.delete<SessionWithDrinks>('/api/session/reset');
    return response.data;
  },

  // Get session history
  getHistory: async (): Promise<SessionWithDrinks[]> => {
    const response = await api.get<SessionWithDrinks[]>('/api/session/history');
    return response.data;
  },
};

// AI recommendations API
export const recommendationApi = {
  // Get AI-powered drink recommendations based on current session
  getRecommendations: async (): Promise<RecommendationResponse> => {
    const response = await api.post<RecommendationResponse>('/api/recommendations');
    return response.data;
  },
};

export default api;
