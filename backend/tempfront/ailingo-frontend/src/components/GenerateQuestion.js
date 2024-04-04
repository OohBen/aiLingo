import React, { useState } from 'react';
import axiosInstance from '../utils/axiosInstance';

function GenerateQuestion() {
  const [quizId, setQuizId] = useState('');
  const [prompt, setPrompt] = useState('');
  const [question, setQuestion] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post(`http://localhost:8000/api/quizzes/${quizId}/generate-question/`, { prompt });
      setQuestion(response.data.question);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Generate Question</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Quiz ID"
          value={quizId}
          onChange={(e) => setQuizId(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          required
        />
        <button type="submit">Generate</button>
      </form>
      {question && (
        <div>
          <h3>Generated Question:</h3>
          <p>{question.text}</p>
          <p>Answer: {question.answer}</p>
        </div>
      )}
    </div>
  );
}

export default GenerateQuestion;