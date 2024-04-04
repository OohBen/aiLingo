import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

function Quizzes() {
  const [quizzes, setQuizzes] = useState([]);

  useEffect(() => {
    fetchQuizzes();
  }, []);

  const fetchQuizzes = async () => {
    try {
      const response = await axiosInstance.get('http://localhost:8000/api/quizzes/');
      setQuizzes(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="quizzes">
      <Container>
        <h2>Quizzes</h2>
        <Row>
          {quizzes.map((quiz) => (
            <Col md={4} key={quiz.id}>
              <Card>
                <Card.Body>
                  <Card.Title>{quiz.title}</Card.Title>
                  <Card.Text>Language: {quiz.language}</Card.Text>
                  <Card.Text>Duration: {quiz.duration} minutes</Card.Text>
                  <Card.Text>Passing Score: {quiz.passing_score}%</Card.Text>
                  <Button variant="primary" as={Link} to={`/quizzes/${quiz.id}`}>
                    Take Quiz
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Container>
    </div>
  );
}

export default Quizzes;