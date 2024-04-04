import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import axiosInstance from '../utils/axiosInstance';

function Profile() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUserData();
    console.log("hello");
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await axiosInstance.get('/users/profile/');
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const handleLogout = async () => {
    try {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      navigate('/login');
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <Container>
      <h1>Profile</h1>
      <Row>
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>User Information</Card.Title>
              <p>Name: {user.name}</p>
              <p>Email: {user.email}</p>
              {/* Display other user information */}
            </Card.Body>
          </Card>
        </Col>
      </Row>
      <Row>
        <Col>
          <Button variant="danger" onClick={handleLogout}>
            Logout
          </Button>
        </Col>
      </Row>
    </Container>
  );
}

export default Profile;