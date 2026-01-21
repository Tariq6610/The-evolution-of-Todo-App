import axios, { AxiosInstance, AxiosError } from "axios";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "https://the-evolution-of-todo-app-production.up.railway.app/api/v1";

console.log(
  "API_CLIENT_DEBUG: Raw environment variable NEXT_PUBLIC_API_URL:",
  process.env.NEXT_PUBLIC_API_URL,
);
console.log("API_CLIENT_DEBUG: Final API_BASE_URL:", API_BASE_URL);

/**
 * Custom API Client based on Axios
 * Configured with base URL and interceptors for authentication
 * Uses cookies for authentication (set by login endpoint)
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 seconds
  withCredentials: true, // Enable cookies for authentication
});

// Add request interceptor to debug the actual request being made
apiClient.interceptors.request.use(
  (config) => {
    console.log(
      "API_CLIENT_DEBUG: Request being made to:",
      config.baseURL + (config.url || ""),
    );
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Request interceptor: (not needed for cookie-based auth, but kept for future)
// apiClient.interceptors.request.use(
//   (config: InternalAxiosRequestConfig) => {
//     return config;
//   },
//   (error: AxiosError) => {
//     return Promise.reject(error);
//   }
// );

// Response interceptor: handle token expiration or global errors
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // If status is 401, token might be expired
    if (error.response?.status === 401) {
      // Clear any client-side state if needed
    }

    // Transform error response for easier handling in components
    const message =
      (error.response?.data as { detail?: string })?.detail || error.message;
    return Promise.reject(new Error(message));
  },
);

export default apiClient;
