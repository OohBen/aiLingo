'use client';

import { useAuth } from '../../lib/useAuth';
import { useEffect, useState } from 'react';
import { getLessons } from '../../lib/api';
import { LessonList } from '../../components/LessonList';

export default function Lessons() {
  const user = useAuth();
  const [lessons, setLessons] = useState([]);

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const data = await getLessons();
        setLessons(data);
      } catch (error) {
        console.error('Failed to fetch lessons', error);
      }
    };

    if (user) {
      fetchLessons();
    }
  }, [user]);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Lessons</h1>
      <LessonList lessons={lessons} />
    </div>
  );
}