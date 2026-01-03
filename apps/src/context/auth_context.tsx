'use client';

import { createContext, useContext, ReactNode, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/services/api_client';

interface AuthContextType {
  user: any | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, password: string, fullName: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in on initial load
    const token = localStorage.getItem('auth_token');
    if (token) {
      // In a real app, you would verify the token and get user details
      // For now, we'll just set a basic user object
      setUser({ id: 'temp', email: localStorage.getItem('user_email') || 'temp' });
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      // Prepare form data as URLSearchParams to match OAuth2PasswordRequestForm expectations
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);

      const response = await apiClient.post('/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        }
      });

      // Store token in localStorage
      localStorage.setItem('auth_token', response.data.access_token);
      localStorage.setItem('user_email', email);
      setUser({ id: 'temp', email });
      router.push('/dashboard');
    } catch (error: any) {
      throw error;
    }
  };

  const register = async (email: string, password: string, fullName: string) => {
    try {
      const response = await apiClient.post('/auth/register', {
        email,
        password,
        full_name: fullName
      });

      // Store token in localStorage
      localStorage.setItem('auth_token', response.data.access_token || response.data.id);
      localStorage.setItem('user_email', email);
      setUser({ id: 'temp', email });
      router.push('/dashboard');
    } catch (error: any) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_email');
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}