import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { useAuth } from './contexts/AuthContext';

function Navigation({ darkMode, toggleDarkMode }) {
    const { loggedIn, logout } = useAuth();


  
    return (
    <Navbar bg={darkMode ? 'dark' : 'light'} variant={darkMode ? 'dark' : 'light'} expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">
          aiLingo
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ml-auto">
            <Nav.Link as={Link} to="/">
              Home
            </Nav.Link>
            {!loggedIn && (
              <>
                <Nav.Link as={Link} to="/register">
                  Register
                </Nav.Link>
                <Nav.Link as={Link} to="/login">
                  Login
                </Nav.Link>
              </>
            )}
            <Nav.Link as={Link} to="/languages">
              Languages
            </Nav.Link>
            <Nav.Link as={Link} to="/lessons">
              Lessons
            </Nav.Link>
            <Nav.Link as={Link} to="/quizzes">
              Quizzes
            </Nav.Link>
            {loggedIn && ( 
              <Nav.Link as={Link} to="/create-quiz">
                Create Quiz
              </Nav.Link>
            )}
            {loggedIn && (
              <Nav.Link as={Link} to="/profile">
                Profile
              </Nav.Link>
            )}
              {loggedIn && (
              <Nav.Link as={Link} to="/chat">
                Chat
              </Nav.Link>
            )}
              {loggedIn && (
              <Nav.Link as={Link} to="/analytics">
                Analytics
              </Nav.Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
      <Button variant={darkMode ? 'light' : 'dark'} onClick={toggleDarkMode}>
        {darkMode ? 'Light Mode' : 'Dark Mode'}
      </Button>
    </Navbar>
);
}

export default Navigation;