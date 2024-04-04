import React, { useState, useEffect } from 'react';
import axiosInstance from '../utils/axiosInstance';
import { useNavigate } from 'react-router-dom';

function CreateQuiz() {
  const [title, setTitle] = useState('');
  const [language, setLanguage] = useState('');
  const [languages, setLanguages] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchLanguages();
  }, []);

  const fetchLanguages = async () => {
    try {
      const response = await axiosInstance.get('http://localhost:8000/api/languages/');
      setLanguages(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const response = await axiosInstance.post('http://localhost:8000/api/quizzes/create/', {
        title,
        language,
        duration: 10,
        passing_score: 50,
      });
      console.log(response.data);
      setSuccess(true);
      setError('');
      setLoading(false);
      navigate('/quizzes');
    } catch (error) {
      console.error(error);
      setError('Failed to create quiz. Please try again.');
      setSuccess(false);
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="create-quiz-form">
        <h2>Create Quiz</h2>
        {success && <p className="success">Quiz created successfully!</p>}
        {error && <p className="error">{error}</p>}
        {loading ? (
          <div className="loading">
            <p>Creating quiz...</p>
            <div className="loading-spinner"></div>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Quiz Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              required
            >
              <option value="">Select Language</option>
              {languages.map((lang) => (
                <option key={lang.id} value={lang.id}>
                  {lang.name}
                </option>
              ))}
            </select>
            <button type="submit">Create Quiz</button>
          </form>
        )}
      </div>
    </div>
  );
}

export default CreateQuiz;