import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

/**
 * Custom API Client based on Axios
 * Configured with base URL and interceptors for authentication
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 seconds
});

// Request interceptor: attach token if present
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("auth_token");
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor: handle token expiration or global errors
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // If status is 401, token might be expired
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        // Clear token and redirect to login if necessary
        localStorage.removeItem("auth_token");
        // We could use window.location.href = '/login' here or let components handle it
      }
    }

    // Transform error response for easier handling in components
    const message = (error.response?.data as { detail?: string })?.detail || error.message;
    return Promise.reject(new Error(message));
  }
);

export default apiClient;
