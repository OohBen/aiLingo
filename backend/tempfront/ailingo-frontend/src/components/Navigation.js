import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { isLoggedIn } from '../utils/auth';

function Navigation() {
  const loggedIn = isLoggedIn();

  return (
    <Navbar bg="dark" variant="dark" expand="lg">
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
              <Nav.Link as={Link} to="/profile">
                Profile
              </Nav.Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Navigation;