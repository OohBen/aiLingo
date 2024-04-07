import axios from 'axios';
import { refreshAccessToken, logoutUser } from './auth';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

axiosInstance.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const access_token = await refreshAccessToken();
        axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // Logout the user if the refresh token is invalid
        logoutUser();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;