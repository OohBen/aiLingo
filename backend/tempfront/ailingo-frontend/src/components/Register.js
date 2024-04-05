import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap';
import { registerUser } from '../utils/auth';
import axiosInstance from '../utils/axiosInstance';

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
    fetchLanguages();
  }, []);

  const fetchLanguages = async () => {
    try {
      const response = await axiosInstance.get('/languages/');
      setLanguages(response.data);
    } catch (error) {
      console.error('Error fetching languages:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerUser(name, email, password, homeLanguage);
      setSuccess(true);
      setError('');
      setTimeout(() => {
        navigate('/dashboard');
      }, 1500);
    } catch (error) {
      setError(error.error);
      setSuccess(false);
    }
  };

  return (
    <Container>
      <Row className="justify-content-center mt-5">
        <Col md={6}>
          <h2>User Registration</h2>
          {success && <Alert variant="success">Registration successful! Redirecting to dashboard...</Alert>}
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
            <Form.Group controlId="email">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="password">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="homeLanguage">
              <Form.Label>Home Language</Form.Label>
              <Form.Control
                as="select"
                value={homeLanguage}
                onChange={(e) => setHomeLanguage(e.target.value)}
                required
              >
                <option value="">Select your home language</option>
                {languages.map((language) => (
                  <option key={language.id} value={language.id}>
                    {language.name}
                  </option>
                ))}
              </Form.Control>
            </Form.Group>
            <Button variant="primary" type="submit" className="mt-3">
              Register
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default Register;