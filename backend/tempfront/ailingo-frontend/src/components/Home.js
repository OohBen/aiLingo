import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <Container>
      <Row className="mt-5">
        <Col>
          <h1>Welcome to aiLingo</h1>
          <p>Learn languages with AI-powered lessons and quizzes.</p>
          <Button as={Link} to="/register" variant="primary" size="lg">
            Get Started
          </Button>
        </Col>
      </Row>
    </Container>
  );
}

export default Home;