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
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Quizzes</h1>
      <QuizList quizzes={quizzes} />
    </div>
  );
}