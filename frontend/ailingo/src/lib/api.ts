import axios, { AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});


axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axiosInstance.post('/users/refresh-token/', {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers['Authorization'] = `Bearer ${access}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);



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
    const response = await axiosInstance.get(`/users/profile/`, {
      params: { email },
    });
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

export const createQuiz = async (quizData: { title: string; language: string }) => {
  try {
    const response = await axiosInstance.post('/quizzes/create/', quizData);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getUserAnalytics = async (email: string) => {
  try {
    const response = await axiosInstance.get(`/analytics/user-analytics/`, {
      params: { email },
    });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// ...

export const getConversations = async () => {
  try {
    const response = await axiosInstance.get('/chat/conversations/');
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const createConversation = async (languageId: string, title: string) => {
  try {
    const response = await axiosInstance.post('/chat/conversations/', { language: languageId, title });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getMessages = async (conversationId: string) => {
  try {
    const response = await axiosInstance.get(`/chat/conversations/${conversationId}/messages/`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const sendMessage = async (conversationId: string, content: string) => {
  try {
    const response = await axiosInstance.post(`/chat/conversations/${conversationId}/messages/`, { content });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getQuizQuestions = async (quizId: number) => {
  try {
    const response = await axiosInstance.get(`/quizzes/${quizId}/questions/`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};
export const submitQuizAttempt = async (attemptData: { quiz: number; user_answers: { [key: number]: number } }) => {
  try {
    const response = await axiosInstance.post('/quizzes/attempt/', attemptData);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};


