import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';

function QuizDetails() {
  const { id } = useParams();
  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [userAnswers, setUserAnswers] = useState({});
  const navigate = useNavigate();
  useEffect(() => {
    fetchQuizDetails();
    fetchQuestions();
  }, []);

  const fetchQuizDetails = async () => {
    try {
      const response = await axiosInstance.get(`http://localhost:8000/api/quizzes/${id}/`);
      setQuiz(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchQuestions = async () => {
    try {
      const response = await axiosInstance.get(`http://localhost:8000/api/quizzes/${id}/questions/`);
      setQuestions(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleAnswerSelect = (questionId, selectedAnswer) => {
    setUserAnswers((prevAnswers) => ({
      ...prevAnswers,
      [questionId]: selectedAnswer,
    }));
  };

  const calculateScore = () => {
    let totalScore = 0;
    let maxScore = 0;

    questions.forEach((question) => {
      maxScore += question.worth;
      if (userAnswers[question.id] === question.answer) {
        totalScore += question.worth;
      }
    });

    return (totalScore / maxScore) * 100;
  };

  const handleQuizSubmit = async () => {
    const attemptData = {
      quiz: quiz.id,
      user_answers: userAnswers,
    };

    try {
      await axiosInstance.post('http://localhost:8000/api/quizzes/attempt/', attemptData);
      // Redirect to the analytics dashboard or display a success message
      navigate('/analytics');
    } catch (error) {
      console.error(error);
    }
  };

  if (!quiz) {
    return <div>Loading...</div>;
  }

  return (
    <div className="quiz-details">
      {/* ... existing code ... */}
      <button onClick={handleQuizSubmit}>Submit Quiz</button>
    </div>
  );
}

export default QuizDetails;