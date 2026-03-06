"use client";

import {
  createContext,
  useContext,
  ReactNode,
  useEffect,
  useState,
} from "react";
import { useRouter } from "next/navigation";
import apiClient from "@/services/api_client";

interface AuthContextType {
  user: { id?: string; email?: string; name?: string; bio?: string } | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (
    email: string,
    password: string,
    fullName: string,
  ) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Helper to check for auth cookie
function hasAuthCookie(): boolean {
  if (typeof document === "undefined") return false;
  return document.cookie
    .split(";")
    .some((c) => c.trim().startsWith("access_token="));
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<{
    id?: string;
    email?: string;
    name?: string;
    bio?: string;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in by making an API call to verify the token
    // Note: We make the API call regardless of hasAuthCookie() result since
    // access_token is HTTP-only and not accessible via JavaScript
    const checkAuthStatus = async () => {
      console.log("[DEBUG] AuthProvider - Starting auth check");
      console.log(
        "[DEBUG] AuthProvider - hasAuthCookie() (will be false for HTTP-only):",
        hasAuthCookie(),
      );
      console.log(
        "[DEBUG] AuthProvider - All cookies (non-HTTP-only only):",
        document.cookie,
      );

      // Always make the API call to check authentication status
      // The access_token cookie will be sent automatically with the request due to withCredentials: true
      console.log(
        "[DEBUG] AuthProvider - Making API call to /auth/me to verify authentication",
      );
      try {
        const response = await apiClient.get("/auth/me", {
          withCredentials: true,
        });
        console.log(
          "[DEBUG] AuthProvider - API call successful, user data:",
          response.data,
        );
        setUser(response.data);
      } catch (error: unknown) {
        const err = error as {
          message?: string;
          response?: { status?: number; data?: { detail?: string } };
        };
        console.log(
          "[DEBUG] AuthProvider - API call failed, error:",
          err.message,
        );
        console.log("[DEBUG] AuthProvider - Error response:", err.response);
        // Token is invalid or expired, clear any stored user info
        document.cookie =
          "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie =
          "user_email=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        setUser(null);
      }
      console.log("[DEBUG] AuthProvider - Setting loading to false");
      setLoading(false);
    };

    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      // Prepare form data as URLSearchParams to match OAuth2PasswordRequestForm expectations
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", password);

      const response = await apiClient.post("/auth/login", params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        withCredentials: true, // Enable cookies
      });

      // Set user email cookie for persistence
      document.cookie = `user_email=${encodeURIComponent(email)}; path=/; max-age=31536000`;

      // Set user state with complete user data and redirect
      setUser({
        id: response.data.user_id,
        email: response.data.email,
      });
      router.push("/dashboard");
    } catch (error: unknown) {
      throw error;
    }
  };

  const register = async (
    email: string,
    password: string,
    fullName: string,
  ) => {
    try {
      const response = await apiClient.post(
        "/auth/register",
        {
          email,
          password,
          full_name: fullName,
        },
        {
          withCredentials: true, // Enable cookies
        },
      );

      // Set user email cookie
      document.cookie = `user_email=${encodeURIComponent(email)}; path=/; max-age=31536000`;

      // Set user state with complete user data and redirect
      setUser({
        id: response.data.id,
        email: response.data.email,
      });
      router.push("/dashboard");
    } catch (error: unknown) {
      throw error;
    }
  };

  const logout = () => {
    // Clear auth cookie
    document.cookie =
      "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie =
      "user_email=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    setUser(null);
    router.push("/login");
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
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
