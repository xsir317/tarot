import { describe, it, expect, beforeEach, vi, Mock } from 'vitest';
import axios from 'axios';
import { useUserStore } from '../../stores/useUserStore';

// Mock axios
vi.mock('axios', () => {
  const mockAxios = {
    create: vi.fn(() => ({
      interceptors: {
        request: { use: vi.fn(), eject: vi.fn() },
        response: { use: vi.fn(), eject: vi.fn() },
      },
      get: vi.fn(),
      post: vi.fn(),
    })),
  };
  return {
    default: mockAxios,
  };
});

// Mock store
vi.mock('../../stores/useUserStore', () => ({
  useUserStore: {
    getState: vi.fn(),
  },
}));

describe('API Client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // We need to reset modules to ensure apiClient re-runs axios.create
    vi.resetModules();
  });

  it('should have interceptors configured', async () => {
    // Import apiClient after mock setup
    await import('../../lib/api-client');
    
    const createMock = axios.create as Mock;
    expect(createMock).toHaveBeenCalled();
    
    const mockInstance = createMock.mock.results[0].value;
    expect(mockInstance.interceptors.request.use).toHaveBeenCalled();
    expect(mockInstance.interceptors.response.use).toHaveBeenCalled();
  });

  it('should attach token to headers if it exists', async () => {
    // Setup store mock
    const mockToken = 'test-token';
    (useUserStore.getState as Mock).mockReturnValue({ token: mockToken });

    // Import apiClient
    await import('../../lib/api-client');

    const createMock = axios.create as Mock;
    const mockInstance = createMock.mock.results[0].value;
    // Get the first call to request.use (success handler is first arg)
    const requestInterceptor = mockInstance.interceptors.request.use.mock.calls[0][0];

    // Simulate a request config
    const config = { headers: {} };
    const result = await requestInterceptor(config);

    expect(result.headers.Authorization).toBe(`Bearer ${mockToken}`);
  });

  it('should NOT attach token if it does not exist', async () => {
    // Setup store mock
    (useUserStore.getState as Mock).mockReturnValue({ token: null });

    // Import apiClient
    await import('../../lib/api-client');

    const createMock = axios.create as Mock;
    const mockInstance = createMock.mock.results[0].value;
    const requestInterceptor = mockInstance.interceptors.request.use.mock.calls[0][0];

    // Simulate a request config
    const config = { headers: {} };
    const result = await requestInterceptor(config);

    expect(result.headers.Authorization).toBeUndefined();
  });
});
