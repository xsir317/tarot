import axios from 'axios';
import { useUserStore } from '@/stores/useUserStore';

// Create axios instance
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = useUserStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    // TODO: Handle 401 Unauthorized (Token Refresh)
    // For MVP, we might just logout or redirect
    if (error.response?.status === 401) {
      // useUserStore.getState().logout();
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
