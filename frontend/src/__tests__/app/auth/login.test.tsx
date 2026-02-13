import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import LoginPage from '@/app/[locale]/auth/login/page';
import { apiClient } from '@/lib/api-client';
import { useUserStore } from '@/stores/useUserStore';
import { NextIntlClientProvider } from 'next-intl';

// Mock dependencies
const mockLogin = vi.fn();

vi.mock('@/lib/api-client', () => ({
  apiClient: {
    post: vi.fn(),
  },
}));

vi.mock('@/stores/useUserStore', () => ({
  useUserStore: Object.assign(
    vi.fn((selector) => selector({ login: mockLogin })),
    {
      getState: () => ({ login: mockLogin }),
    }
  ),
}));

// Mock router
const mockPush = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

// Mock translations
const messages = {
  Auth: {
    login_title: "Login",
    login_description: "Enter your phone number to continue",
    phone_label: "Phone Number",
    code_label: "Verification Code",
    send_code: "Send Code",
    login_button: "Login",
    code_sent: "Code sent!",
    login_success: "Login successful!",
    send_code_failed: "Failed to send code",
    login_failed: "Login failed",
    loading: "Loading..."
  }
};

const renderWithIntl = (component: React.ReactNode) => {
  return render(
    <NextIntlClientProvider locale="en" messages={messages}>
      {component}
    </NextIntlClientProvider>
  );
};

describe('LoginPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.spyOn(window, 'alert').mockImplementation(() => {});
  });

  it('renders login form', () => {
    renderWithIntl(<LoginPage />);
    expect(screen.getByRole('heading', { name: 'Login' })).toBeDefined();
    expect(screen.getByLabelText('Phone Number')).toBeDefined();
    expect(screen.getByLabelText('Verification Code')).toBeDefined();
  });

  it('handles send code flow', async () => {
    (apiClient.post as any).mockResolvedValueOnce({ 
      data: { data: { code: '123456' } } 
    });

    renderWithIntl(<LoginPage />);
    
    const phoneInput = screen.getByLabelText('Phone Number');
    fireEvent.change(phoneInput, { target: { value: '1234567890' } });
    
    const sendButton = screen.getByText('Send Code');
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/auth/send-code', {
        phone: '1234567890'
      });
    });
  });

  it('handles login flow', async () => {
    (apiClient.post as any).mockResolvedValueOnce({ 
      data: { 
        data: { 
          access_token: 'at', 
          refresh_token: 'rt', 
          user: { id: '1' } 
        } 
      } 
    });

    renderWithIntl(<LoginPage />);
    
    // Fill form
    fireEvent.change(screen.getByLabelText('Phone Number'), { target: { value: '1234567890' } });
    fireEvent.change(screen.getByLabelText('Verification Code'), { target: { value: '123456' } });
    
    // Submit
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/auth/login/code', {
        phone: '1234567890',
        code: '123456'
      });
      expect(mockLogin).toHaveBeenCalledWith(
        { id: '1' }, 
        'at', 
        'rt'
      );
      expect(mockPush).toHaveBeenCalledWith('/en');
    });
  });
});
