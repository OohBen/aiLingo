import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';

function QuizAttempt() {
  const { id } = useParams();
  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [userAnswers, setUserAnswers] = useState({});
  const [score, setScore] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchQuizDetails();
    fetchQuestions();
  }, [id]);

  const fetchQuizDetails = async () => {
    try {
      const response = await axiosInstance.get(`quizzes/${id}/`);
      setQuiz(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchQuestions = async () => {
    try {
      const response = await axiosInstance.get(`quizzes/${id}/questions/`);
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
  const isSubmitDisabled = () => {
    return questions.some((question) => !userAnswers.hasOwnProperty(question.id));
  };
  const handleQuizSubmit = async () => {
    try {
      const response = await axiosInstance.post('quizzes/attempt/', {
        quiz: quiz.id,
        user_answers: userAnswers,
      });
      setScore(response.data.score);
    } catch (error) {
      console.error(error);
    }
  };

  if (!quiz || questions.length === 0) {
    return <div>Loading...</div>;
  }

  return (
    <div className="quiz-attempt">
      <h2>{quiz.title}</h2>
      <h3>Questions:</h3>
      <ul>
        {questions.map((question) => (
          <li key={question.id} className="question-item">
            <div className="question-text">{question.text}</div>
            <ul className="question-choices">
              {question.choices.map((choice, index) => (
                <li
                  key={index}
                  className={`choice ${
                    userAnswers[question.id] === index + 1 ? 'selected' : ''
                  }`}
                  onClick={() => handleAnswerSelect(question.id, index + 1)}
                >
                  {choice}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
      {score === null ? (
        <button onClick={handleQuizSubmit} disabled={isSubmitDisabled()}>
          Submit Quiz
        </button>
      ) : (
        <div>
          <h3>Score: {score}%</h3>
          <button onClick={() => navigate('/analytics')}>View Analytics</button>
        </div>
      )}
    </div>
  );
}


export default QuizAttempt;