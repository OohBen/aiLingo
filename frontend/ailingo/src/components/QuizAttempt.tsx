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
      <div className="bg-white shadow-lg rounded-lg p-8">
        <h2 className="text-3xl font-bold mb-6">Quiz Result</h2>
        <p className="text-xl mb-8">Your score: {score}%</p>
        <div className="space-y-6">
          {result.map((item, index) => (
            <div key={index} className="border border-gray-300 rounded-lg p-6">
              <p className="text-lg font-semibold mb-2">{item.question}</p>
              <p className="mb-2">Your Answer: {item.user_answer}</p>
              <p className="mb-2">Correct Answer: {item.correct_answer}</p>
              {item.explanation && (
                <p className="text-green-600">{item.explanation}</p>
              )}
            </div>
          ))}
        </div>
        <button
          onClick={handleReset}
          className="mt-8 bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-blue-700"
        >
          Retry Quiz
        </button>
      </div>
    );
  }

  const question = questions[currentQuestion];
  if (!question) {
    return <div className="text-xl font-semibold">Loading question...</div>;
  }

  return (
    <div className="bg-white shadow-lg rounded-lg p-8">
      <h2 className="text-3xl font-bold mb-6">{question.text}</h2>
      <div className="space-y-4">
        {question.choices.map((choice, index) => (
          <div key={index} className="flex items-center">
            <input
              type="radio"
              id={`answer-${question.id}-${index}`}
              className="form-radio h-5 w-5 text-blue-600"
              name={`answer-${question.id}`}
              value={index}
              checked={selectedAnswers[question.id] === index}
              onChange={() => handleAnswerSelect(question.id, index)}
            />
            <label htmlFor={`answer-${question.id}-${index}`} className="ml-3 text-lg">
              {choice}
            </label>
          </div>
        ))}
      </div>
      <button
        onClick={handleNext}
        className="mt-8 bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-blue-700"
      >
        {currentQuestion === questions.length - 1 ? 'Submit' : 'Next'}
      </button>
    </div>
  );
}