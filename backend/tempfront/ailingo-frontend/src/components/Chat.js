// Chat.js

import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, Button, Card } from 'react-bootstrap';
import axiosInstance from '../utils/axiosInstance';
import { Link } from 'react-router-dom';

function Chat( ) {
    const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [newConversationLanguage, setNewConversationLanguage] = useState('');
  const [languages, setLanguages] = useState([]);
  const [isSuperuser, setIsSuperuser] = useState(false);
  const [homeLanguage, setHomeLanguage] = useState('');
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    fetchConversations();
    fetchLanguages();
    checkSuperuser();
    fetchHomeLanguage();
  }, []);

  useEffect(() => {
    if (selectedConversation) {
      fetchMessages();
    }
  }, [selectedConversation]);

  const fetchConversations = async () => {
    try {
      const response = await axiosInstance.get('/chat/conversations/');
      setConversations(response.data);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
  };

  const fetchMessages = async () => {
    try {
      const response = await axiosInstance.get(`/chat/conversations/${selectedConversation.id}/messages/`);
      setMessages(response.data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const fetchLanguages = async () => {
    try {
      const response = await axiosInstance.get('/languages/');
      setLanguages(response.data);
    } catch (error) {
      console.error('Error fetching languages:', error);
    }
  };

  const checkSuperuser = async () => {
    try {
      const response = await axiosInstance.get('/users/profile/');
      setIsSuperuser(response.data.is_superuser);
    } catch (error) {
      console.error('Error checking superuser status:', error);
    }
  };

  const fetchHomeLanguage = async () => {
    try {
      const response = await axiosInstance.get('/users/profile/');
      setHomeLanguage(response.data.home_language.name);
    } catch (error) {
      console.error('Error fetching home language:', error);
    }
  };

  const handleConversationClick = (conversation) => {
    setSelectedConversation(conversation);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post(`/chat/conversations/${selectedConversation.id}/messages/`, {
        content: newMessage,
      });
      setMessages([...messages, response.data]);
      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleNewConversation = async (e) => {
    e.preventDefault();
    try {
      const selectedLanguage = languages.find(
        (lang) => lang.id === parseInt(newConversationLanguage)
      );
      const response = await axiosInstance.post('/chat/conversations/', {
        language: selectedLanguage,
      });
      setConversations([...conversations, response.data]);
      setNewConversationLanguage('');
    } catch (error) {
      console.error('Error creating new conversation:', error);
    }
  };

  const handleAddLanguage = async (e) => {
    e.preventDefault();
    const languageName = prompt('Enter the name of the new language:');
    const languageCode = prompt('Enter the code for the new language:');
    if (languageName && languageCode) {
      try {
        const response = await axiosInstance.post('/languages/', {
          name: languageName,
          code: languageCode,
        });
        setLanguages([...languages, response.data]);
      } catch (error) {
        console.error('Error adding new language:', error);
      }
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <Container className={darkMode ? 'dark-mode' : ''}>
      <Row>
        <Col md={4}>
          <Card className={`mb-3 ${darkMode ? 'bg-dark text-light' : ''}`}>
            <Card.Body>
              <Card.Title>Conversations</Card.Title>
              <ul className="list-group">
                {conversations.map((conversation) => (
                  <li
                    key={conversation.id}
                    className={`list-group-item ${darkMode ? 'bg-dark text-light' : ''}`}
                  >
                    <Link to={`/conversations/${conversation.id}`} className="text-decoration-none">
                      {conversation.language.name}
                    </Link>
                  </li>
                ))}
              </ul>
              <Form onSubmit={handleNewConversation} className="mt-3">
                <Form.Group controlId="newConversationLanguage">
                  <Form.Control
                    as="select"
                    value={newConversationLanguage}
                    onChange={(e) => setNewConversationLanguage(e.target.value)}
                    required
                    className={darkMode ? 'bg-dark text-light' : ''}
                  >
                    <option value="">Select Language</option>
                    {languages.map((language) => (
                      <option key={language.id} value={language.id}>
                        {language.name}
                      </option>
                    ))}
                  </Form.Control>
                </Form.Group>
                <Button variant={darkMode ? 'light' : 'primary'} type="submit" className="mt-2">
                  New Conversation
                </Button>
              </Form>
              {isSuperuser && (
                <Button
                  variant={darkMode ? 'light' : 'secondary'}
                  onClick={handleAddLanguage}
                  className="mt-2"
                >
                  Add Language
                </Button>
              )}
            </Card.Body>
          </Card>
        </Col>
        <Col md={8}>
          <Card className={`mb-3 ${darkMode ? 'bg-dark text-light' : ''}`}>
            <Card.Body>
              <Card.Title>Select a conversation to start chatting.</Card.Title>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
export default Chat;