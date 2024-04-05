import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import axiosInstance from '../utils/axiosInstance';
import { logoutUser } from '../utils/auth';

function Profile() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await axiosInstance.get('/users/profile/');
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const handleLogout = () => {
    logoutUser();
    navigate('/login');
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <Container>
      <Row className="justify-content-center mt-5">
        <Col md={6}>
          <Card>
            <Card.Body>
              <Card.Title>Profile</Card.Title>
              <Card.Text>
                <strong>Name:</strong> {user.name}
              </Card.Text>
              <Card.Text>
                <strong>Email:</strong> {user.email}
              </Card.Text>
              <Button variant="primary" onClick={handleLogout}>
                Logout
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default Profile;