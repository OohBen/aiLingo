'use client';

import { Quiz, Question } from '../types';
import { useState } from 'react';

type QuizAttemptProps = {
  quiz: Quiz;
};

export function QuizAttempt({ quiz }: QuizAttemptProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [score, setScore] = useState(0);
  const [showResult, setShowResult] = useState(false);

  const handleAnswerSelect = (answer: string) => {
    setSelectedAnswer(answer);
  };

  const handleSubmit = () => {
    if (selectedAnswer === quiz.questions[currentQuestion].correctAnswer) {
      setScore(score + 1);
    }

    if (currentQuestion === quiz.questions.length - 1) {
      setShowResult(true);
    } else {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer('');
    }
  };

  const handleReset = () => {
    setCurrentQuestion(0);
    setSelectedAnswer('');
    setScore(0);
    setShowResult(false);
  };

  if (showResult) {
    return (
      <div className="bg-white shadow-md rounded-lg p-4">
        <h2 className="text-xl font-semibold mb-4">Quiz Result</h2>
        <p className="mb-4">
          Your score: {score}/{quiz.questions.length}
        </p>
        <button
          onClick={handleReset}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg"
        >
          Retry Quiz
        </button>
      </div>
    );
  }

  const question = quiz.questions[currentQuestion];

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">{question.text}</h2>
      <div className="space-y-2">
        {question.options.map((option, index) => (
          <div key={index}>
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio"
                name="answer"
                value={option}
                checked={selectedAnswer === option}
                onChange={() => handleAnswerSelect(option)}
              />
              <span className="ml-2">{option}</span>
            </label>
          </div>
        ))}
      </div>
      <button
        onClick={handleSubmit}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg"
      >
        {currentQuestion === quiz.questions.length - 1 ? 'Finish' : 'Next'}
      </button>
    </div>
  );
}