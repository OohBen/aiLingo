import React, { useEffect, useState } from 'react';
import axiosInstance from '../utils/axiosInstance';

function Lessons() {
  const [lessons, setLessons] = useState([]);

  useEffect(() => {
    fetchLessons();
  }, []);

  const fetchLessons = async () => {
    try {
      const response = await axiosInstance.get('/lessons/');
      setLessons(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Lessons</h2>
      <ul>
        {lessons.map((lesson) => (
          <li key={lesson.id}>{lesson.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default Lessons;