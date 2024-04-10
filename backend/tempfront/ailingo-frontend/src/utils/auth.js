import axios from 'axios';
import axiosInstance from './axiosInstance';

const BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://ailingo.onrender.com/api';

export const loginUser = async (email, password) => {
  try {
    const response = await axios.post(`${BASE_URL}/users/login/`, { email, password });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    localStorage.setItem('user', JSON.stringify(response.data.user)); // Store user object
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const registerUser = async (name, email, password, homeLanguage) => {
  try {
    const response = await axiosInstance.post('users/register/', {
      name,
      email,
      password,
      home_language: homeLanguage,
    });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) {
    throw new Error('Refresh token not found');
  }

  try {
    const response = await axios.post(`${BASE_URL}/users/refresh-token/`, { refresh: refreshToken });
    localStorage.setItem('access_token', response.data.access);
    return response.data.access;
  } catch (error) {
    // Remove the invalid refresh token from local storage
    localStorage.removeItem('refresh_token');
    throw error.response.data;
  }
};

export const logoutUser = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
};

export const isLoggedIn = () => {
    const accessToken = localStorage.getItem('access_token');
    return !!accessToken;
  };