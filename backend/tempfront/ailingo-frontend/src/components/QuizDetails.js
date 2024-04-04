import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';

function QuizDetails() {
  const { id } = useParams();
  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [score, setScore] = useState(0);

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
    setQuestions((prevQuestions) =>
      prevQuestions.map((question) =>
        question.id === questionId
          ? { ...question, selectedAnswer, showExplanation: true }
          : question
      )
    );
  };

  const handleQuizSubmit = async () => {
    const attemptData = {
      quiz: quiz.id,
      score: score,
    };

    try {
      await axiosInstance.post('http://localhost:8000/api/quizzes/attempt/', attemptData);
      // Redirect to a quiz results page or display a success message
    } catch (error) {
      console.error(error);
    }
  };

  if (!quiz) {
    return <div>Loading...</div>;
  }

  return (
    <div className="quiz-details">
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
                    question.selectedAnswer === index + 1 ? 'selected' : ''
                  } ${
                    question.showExplanation && question.selectedAnswer === index + 1
                      ? question.answer === index + 1
                        ? 'correct'
                        : 'incorrect'
                      : ''
                  }`}
                  onClick={() => handleAnswerSelect(question.id, index + 1)}
                >
                  {choice}
                  {question.showExplanation && question.selectedAnswer === index + 1 && (
                    <span className="choice-icon">
                      {question.answer === index + 1 ? '✔' : '✘'}
                    </span>
                  )}
                  {question.showExplanation && question.selectedAnswer === index + 1 && (
                    <div className="choice-explanation">
                      <strong>Explanation:</strong> {question.explanations[index]}
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
      <button onClick={handleQuizSubmit}>Submit Quiz</button>
    </div>
  );
}

export default QuizDetails;