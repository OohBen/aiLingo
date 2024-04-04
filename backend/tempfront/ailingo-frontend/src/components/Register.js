import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import { Form, Button, Alert } from 'react-bootstrap';

function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [homeLanguage, setHomeLanguage] = useState('');
  const [languages, setLanguages] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the user is already logged in
    const token = localStorage.getItem('access_token');
    if (token) {
      navigate('/profile');
    }
    else {
      fetchLanguages();
    }
  }, [navigate]);

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
      const response = await axios.post('http://localhost:8000/api/users/register/', {
        name,
        email,
        password,
        home_language: homeLanguage,
      });
      console.log(response.data);
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      setSuccess(true);
      setError('');
      navigate('/dashboard');
    } catch (error) {
      console.error(error);
      setError('Registration failed. Please try again.');
      setSuccess(false);
    }
  };

  return (
    <div className="register">
      <h2>User Registration</h2>
      {success && <Alert variant="success">Registration successful! You can now log in.</Alert>}
      {error && <Alert variant="danger">{error}</Alert>}
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="name">
          <Form.Label>Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </Form.Group>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <select
          value={homeLanguage}
          onChange={(e) => setHomeLanguage(e.target.value)}
          required
        >
          <option value="">Select Home Language</option>
          {languages.map((language) => (
            <option key={language.id} value={language.id}>
              {language.name}
            </option>
          ))}
        </select>
        <Button variant="primary" type="submit">Register</Button>
        </Form>
    </div>
  );
}

export default Register;