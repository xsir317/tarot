import { describe, it, expect, beforeEach, vi } from 'vitest';
import { create } from 'zustand';
import { useUserStore } from '../../stores/useUserStore';

// Mock storage
const localStorageMock = (function () {
  let store: Record<string, string> = {};
  return {
    getItem(key: string) {
      return store[key] || null;
    },
    setItem(key: string, value: string) {
      store[key] = value.toString();
    },
    removeItem(key: string) {
      delete store[key];
    },
    clear() {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('useUserStore', () => {
  beforeEach(() => {
    useUserStore.getState().logout();
    localStorage.clear();
  });

  it('should initialize with default values', () => {
    const state = useUserStore.getState();
    expect(state.user).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(state.token).toBeNull();
  });

  it('should set user and token on login', () => {
    const mockUser = { id: '123', nickname: 'Test User' };
    const mockToken = 'mock-token';
    const mockRefreshToken = 'mock-refresh-token';

    useUserStore.getState().login(mockUser, mockToken, mockRefreshToken);

    const state = useUserStore.getState();
    expect(state.user).toEqual(mockUser);
    expect(state.token).toBe(mockToken);
    expect(state.isAuthenticated).toBe(true);
    expect(localStorage.getItem('token')).toBe(mockToken);
  });

  it('should clear state on logout', () => {
    // Setup initial state
    useUserStore.getState().login({ id: '123' }, 'token', 'refresh');
    
    // Perform logout
    useUserStore.getState().logout();

    const state = useUserStore.getState();
    expect(state.user).toBeNull();
    expect(state.token).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(localStorage.getItem('token')).toBeNull();
  });
});
