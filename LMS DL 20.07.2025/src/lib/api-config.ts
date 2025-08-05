// API Configuration for Library Management System
export const API_CONFIG = {
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000",
  endpoints: {
    // Auth endpoints
    login: "/api/auth/login",
    register: "/api/auth/register",
    logout: "/api/auth/logout",

    // Book endpoints
    books: "/api/books",
    book: (id: string) => `/api/books/${id}`,
    bookSearch: "/api/books/search",

    // User endpoints
    users: "/api/users",
    user: (id: string) => `/api/users/${id}`,
    userProfile: "/api/users/profile",

    // Borrowing endpoints
    borrow: "/api/borrow",
    return: "/api/return",
    borrowHistory: "/api/borrow/history",

    // Admin endpoints
    adminStats: "/api/admin/stats",
    adminUsers: "/api/admin/users",
    adminBooks: "/api/admin/books",
  },

  // Request configuration
  headers: {
    "Content-Type": "application/json",
  },

  // Timeout for requests
  timeout: 10000,
};

// Helper function to get full API URL
export const getApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.baseURL}${endpoint}`;
};

// Helper function to get auth headers
export const getAuthHeaders = (): Record<string, string> => {
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;
  return {
    ...API_CONFIG.headers,
    ...(token && { Authorization: `Bearer ${token}` }),
  };
};
