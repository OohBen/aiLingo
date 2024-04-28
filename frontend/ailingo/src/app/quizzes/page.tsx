'use client';

import { useAuth } from '../../lib/useAuth';
import { useEffect, useState } from 'react';
import { getQuizzes } from '../../lib/api';
import { QuizList } from '../../components/QuizList';

export default function Quizzes() {
  const user = useAuth();
  const [quizzes, setQuizzes] = useState([]);

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const data = await getQuizzes();
        setQuizzes(data);
      } catch (error) {
        console.error('Failed to fetch quizzes', error);
      }
    };

    if (user) {
      fetchQuizzes();
    }
  }, [user]);

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-2xl font-bold">Loading...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Quizzes</h1>
      <div className="bg-white rounded-lg shadow-lg p-8">
        <QuizList quizzes={quizzes} />
      </div>
    </div>
  );
}