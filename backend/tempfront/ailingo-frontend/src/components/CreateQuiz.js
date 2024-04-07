import React, { useState, useEffect } from 'react';
import axiosInstance from '../utils/axiosInstance';
import { useNavigate } from 'react-router-dom';
import { Form, Button, Alert } from 'react-bootstrap';

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
      const response = await axiosInstance.get('/languages/');
      setLanguages(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const response = await axiosInstance.post('/quizzes/create/', {
        title,
        language,
      });
      if (response.data.questions && response.data.questions.length > 0) {
        setSuccess(true);
        setError('');
        setLoading(false);
        navigate('/quizzes');
      } else {
        setError('Failed to generate quiz questions.');
        setSuccess(false);
        setLoading(false);
      }
    } catch (error) {
      console.error(error);
      setError('Failed to create quiz. Please try again.');
      setSuccess(false);
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Create Quiz</h2>
      {success && <Alert variant="success">Quiz created successfully!</Alert>}
      {error && <Alert variant="danger">{error}</Alert>}
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="title">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter quiz title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group controlId="language">
          <Form.Label>Language</Form.Label>
          <Form.Control
            as="select"
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
          </Form.Control>
        </Form.Group>
        <Button variant="primary" type="submit" disabled={loading}>
          {loading ? 'Creating...' : 'Create Quiz'}
        </Button>
      </Form>
    </div>
  );
}

export default CreateQuiz;