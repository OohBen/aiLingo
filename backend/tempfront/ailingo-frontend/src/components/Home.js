import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';

function Home() {
  return (
    <div className="home">
      <Container>
        <Row className="hero">
          <Col>
            <h1>Welcome to aiLingo</h1>
            <p>Explore languages, lessons, and quizzes.</p>
            <Button variant="primary" size="lg">Get Started</Button>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Home;