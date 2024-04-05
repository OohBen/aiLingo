import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, Button, Card } from 'react-bootstrap';
import axiosInstance from '../utils/axiosInstance';
import { Link } from 'react-router-dom';
import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

function Chat() {
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
        content: `Please respond using only markdown:\n\n${newMessage}`,
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

  const renderMarkdown = (content) => {
    const processedContent = content.replace(/\\n/g, '\n');
    return <Markdown remarkPlugins={[remarkGfm]}>{processedContent}</Markdown>

  };

  return (
    <Container fluid className={`chat-container ${darkMode ? 'dark-mode' : ''}`}>
      <Row>
        <Col md={3}>
          <Card className={`mb-3 ${darkMode ? 'bg-dark text-light' : ''}`}>
            <Card.Body>
              <Card.Title>Conversations</Card.Title>
              <ul className="list-group">
                {conversations.map((conversation) => (
                  <li
                    key={conversation.id}
                    className={`list-group-item ${
                      conversation === selectedConversation ? 'active' : ''
                    } ${darkMode ? 'bg-dark text-light' : ''}`}
                    onClick={() => handleConversationClick(conversation)}
                  >
                    {conversation.language.name}
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
        <Col md={9}>
          {selectedConversation ? (
            <Card className={`mb-3 ${darkMode ? 'bg-dark text-light' : ''}`}>
              <Card.Body>
                <Card.Title>{selectedConversation.language.name} Conversation</Card.Title>
                <div className="messages">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`message ${
                        message.sender === 'user' ? 'user-message' : 'ai-message'
                      } ${darkMode ? 'bg-secondary text-light' : ''}`}
                    >
                      <strong>{message.sender === 'user' ? 'You' : 'AI Teacher'}:</strong>
                      <div className="message-content">
                        {renderMarkdown(message.content)}
                      </div>
                    </div>
                  ))}
                </div>
                <Form onSubmit={handleSendMessage}>
                  <Form.Group controlId="newMessage" className={`mb-3 ${darkMode ? 'bg-dark' : ''}`}>
                    <Form.Control
                      as="textarea"
                      rows={3}
                      placeholder="Type your message..."
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      required
                      className={`${darkMode ? 'bg-dark text-light' : ''}`}
                    />
                  </Form.Group>
                  <Button variant={darkMode ? 'light' : 'primary'} type="submit">
                    Send
                  </Button>
                </Form>
              </Card.Body>
            </Card>
          ) : (
            <Card className={`mb-3 ${darkMode ? 'bg-dark text-light' : ''}`}>
              <Card.Body>
                <Card.Title>Select a conversation to start chatting.</Card.Title>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default Chat;