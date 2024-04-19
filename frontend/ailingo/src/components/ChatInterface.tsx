'use client';

import axios, { AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

const handleError = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    throw error.response?.data;
  }
  throw error;
};

export const login = async (email: string, password: string) => {
  try {
    const response = await axiosInstance.post('/users/login/', { email, password });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const registerUser = async (name: string, email: string, password: string) => {
  try {
    const response = await axiosInstance.post('/users/register/', { name, email, password });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getUserDetails = async (email: string) => {
  try {
    const response = await axiosInstance.get(`/users/profile/`, { params: { email } });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getLanguages = async () => {
  try {
    const response = await axiosInstance.get('/languages/');
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getLessons = async () => {
  try {
    const response = await axiosInstance.get('/lessons/');
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getQuizzes = async () => {
  try {
    const response = await axiosInstance.get('/quizzes/');
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getQuizById = async (id: string) => {
  try {
    const response = await axiosInstance.get(`/quizzes/${id}/`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const createQuiz = async (title: string, description: string) => {
  try {
    const response = await axiosInstance.post('/quizzes/', { title, description });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getUserAnalytics = async (email: string) => {
  try {
    const response = await axiosInstance.get(`/analytics/user-analytics/`, { params: { email } });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const sendMessage = async (message: string) => {
  try {
    const response = await axiosInstance.post('/chat/', { message });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

