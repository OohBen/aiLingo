// src/components/QuizAttempt.tsx
'use client';

import { Quiz, Question } from '../types';
import { useState, useEffect } from 'react';
import { getQuizQuestions, submitQuizAttempt } from '../lib/api';

type QuizAttemptProps = {
  quiz: Quiz;
};

export function QuizAttempt({ quiz }: QuizAttemptProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<{ [key: number]: number }>({});
  const [score, setScore] = useState(0);
  const [result, setResult] = useState([]);
  const [showResult, setShowResult] = useState(false);
  const [questions, setQuestions] = useState<Question[]>([]);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const data = await getQuizQuestions(quiz.id);
        setQuestions(data);
      } catch (error) {
        console.error('Failed to fetch questions:', error);
      }
    };

    fetchQuestions();
  }, [quiz.id]);

  const handleAnswerSelect = (questionId: number, answer: number) => {
    setSelectedAnswers((prevAnswers) => ({
      ...prevAnswers,
      [questionId]: answer,
    }));
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion((prevQuestion) => prevQuestion + 1);
    } else {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    try {
      const attemptData = {
        quiz: quiz.id,
        user_answers: selectedAnswers,
      };
      const { attempt, result } = await submitQuizAttempt(attemptData);
      setScore(attempt.score);
      setResult(result);
      setShowResult(true);
    } catch (error) {
      console.error('Failed to submit quiz attempt:', error);
    }
  };
  const handleReset = () => {
    setCurrentQuestion(0);
    setSelectedAnswers({});
    setScore(0);
    setShowResult(false);
  };

  if (showResult) {
    return (
      <div className="bg-white shadow-md rounded-lg p-4">
        <h2 className="text-xl font-semibold mb-4">Quiz Result</h2>
        <p className="mb-4">
          Your score: {score}%
        </p>
        <div className="space-y-4">
          {result.map((item, index) => (
            <div key={index}>
              <p className="font-semibold">{item.question}</p>
              <p>Your Answer: {item.user_answer}</p>
              <p>Correct Answer: {item.correct_answer}</p>
              {item.explanation && (
                <p className="text-green-600">Explanation: {item.explanation}</p>
              )}
            </div>
          ))}
        </div>
        <button
          onClick={handleReset}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg"
        >
          Retry Quiz
        </button>
      </div>
    );
  }
    

  const question = questions[currentQuestion];

  if (!question) {
    return <div>Loading question...</div>;
  }

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">{question.text}</h2>
      <div className="space-y-2">
        {question.choices.map((choice, index) => (
          <div key={index}>
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio"
                name={`answer-${question.id}`}
                value={index}
                checked={selectedAnswers[question.id] === index}
                onChange={() => handleAnswerSelect(question.id, index)}
              />
              <span className="ml-2">{choice}</span>
            </label>
          </div>
        ))}
      </div>
      <button
        onClick={handleNext}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg"
      >
        {currentQuestion === questions.length - 1 ? 'Submit' : 'Next'}
      </button>
    </div>
  );
}