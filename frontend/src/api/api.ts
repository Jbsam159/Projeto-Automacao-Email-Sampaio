import axios from "axios";
import type { InternalAxiosRequestConfig } from "axios";
import { logout } from "./auth";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL // backend FastAPI
});

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem("access_token");

    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      logout();
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

export default api;
