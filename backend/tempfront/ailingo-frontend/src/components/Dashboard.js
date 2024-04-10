// src/components/Dashboard.js
import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { useAuth } from './contexts/AuthContext';

function Dashboard() {
  const { user } = useAuth();

  return (
    <Container>
      <Row className="mt-5">
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>Welcome to the Dashboard</Card.Title>
              {user && (
                <Card.Text>
                  <strong>Name:</strong> {user.name}
                  <br />
                  <strong>Email:</strong> {user.email}
                </Card.Text>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default Dashboard;