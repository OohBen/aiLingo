import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export const getLanguages = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/languages`);
    return response.data;
  } catch (error) {
    console.error('There was an error fetching the languages', error);
    throw error;
  }
};

export const getLessonsForLanguage = async (languageId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/languages/${languageId}/lessons`);
    return response.data;
  } catch (error) {
    console.error('There was an error fetching the lessons', error);
    throw error;
  }
};
export const createConversation = async (languageId, title) => {
  try {
    const response = await axiosInstance.post('/chat/conversations/', { language: languageId, title });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getQuizzesForLanguage = async (languageId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/languages/${languageId}/quizzes`);
    return response.data;
  } catch (error) {
    console.error('There was an error fetching the quizzes', error);
    throw error;
  }
};

export const getLesson = async (lessonId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/lessons/${lessonId}`);
    return response.data;
  } catch (error) {
    console.error('There was an error fetching the lesson', error);
    throw error;
  }
};



export const getQuiz = async (quizId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/quizzes/${quizId}`);
    return response.data;
  } catch (error) {
    console.error('There was an error fetching the quiz', error);
    throw error;
  }
};
