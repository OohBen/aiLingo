// src/components/Profile.js
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Card, Button, Form } from 'react-bootstrap';
import axiosInstance from '../utils/axiosInstance';
import { logoutUser } from '../utils/auth';

function Profile() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [profilePic, setProfilePic] = useState(null);

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

  const handleProfilePicChange = (e) => {
    setProfilePic(e.target.files[0]);
  };

  const handleUpdateProfilePic = async () => {
    try {
      const formData = new FormData();
      formData.append('profile_pic', profilePic);

      await axiosInstance.patch('/users/profile/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Refresh user data after updating profile picture
      fetchUserData();
    } catch (error) {
      console.error('Error updating profile picture:', error);
    }
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
              {user.profile_pic && (
                <Card.Img
                  variant="top"
                  src={user.profile_pic}
                  alt="Profile Picture"
                  className="mb-3"
                />
              )}
              <Button variant="primary" onClick={handleLogout}>
                Logout
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      <Row className="justify-content-center mt-3">
        <Col md={6}>
          <Form.Group controlId="profilePic">
            <Form.Label>Profile Picture</Form.Label>
            <Form.Control type="file" onChange={handleProfilePicChange} />
          </Form.Group>
          <Button variant="primary" onClick={handleUpdateProfilePic} className="mt-3">
            Update Profile Picture
          </Button>
        </Col>
      </Row>
    </Container>
  );
}

export default Profile;