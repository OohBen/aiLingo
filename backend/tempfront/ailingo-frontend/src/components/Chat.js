import React, { useState, useEffect, useRef } from 'react';
import { Container, Row, Col, Form, Button, Card } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function Chat() {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [newConversationLanguage, setNewConversationLanguage] = useState('');
  const [newConversationTitle, setNewConversationTitle] = useState('');
  const [languages, setLanguages] = useState([]);
  const [isSuperuser, setIsSuperuser] = useState(false);
  const [homeLanguage, setHomeLanguage] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchConversations();
    fetchLanguages();
    checkSuperuser();
    fetchHomeLanguage();
  }, []);

  useEffect(() => {
    if (selectedConversation) {
      fetchMessages();
      scrollToBottom();
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
    if (isLoading) return;

    setIsLoading(true);

    try {
      const response = await axiosInstance.post(`/chat/conversations/${selectedConversation.id}/messages/`, {
        content: newMessage,
      });
      setMessages([...messages, { sender: 'user', content: newMessage }, response.data]);
      setNewMessage('');

      if (response.data.content.includes('Quiz created successfully!')) {
        const quizLink = response.data.content.match(/\/quizzes\/\d+/)[0];
        navigate(quizLink);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewConversation = async (e) => {
    e.preventDefault();
    try {
      const selectedLanguage = languages.find(
        (lang) => lang.id === parseInt(newConversationLanguage)
      );
      if (!newConversationTitle) {
        setNewConversationTitle(prompt('Enter a title for the new conversation:'));
      }
      if (newConversationTitle && selectedLanguage) {
        const response = await axiosInstance.post('/chat/conversations/', {
          language: selectedLanguage,
          title: newConversationTitle,
        });
        setConversations([...conversations, response.data]);
        setSelectedConversation(response.data);
        setNewConversationLanguage('');
        setNewConversationTitle('');
      }
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

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const renderMarkdown = (content) => {
    return <Markdown remarkPlugins={[remarkGfm]}>{content}</Markdown>;
  };

  return (
    <Container fluid className={`chat-container ${darkMode ? 'dark-mode' : ''}`}>
      <Row>
        <Col md={3}>
          <Card className={`conversations-card ${darkMode ? 'dark-mode' : ''}`}>
            <Card.Header>
              <h4>Conversations</h4>
            </Card.Header>
            <Card.Body>
              <ul className="list-unstyled">
                {conversations.map((conversation) => (
                  <li
                    key={conversation.id}
                    className={`conversation-item ${
                      conversation === selectedConversation ? 'active' : ''
                    } ${darkMode ? 'dark-mode' : ''}`}
                    onClick={() => handleConversationClick(conversation)}
                  >
                    {conversation.title} ({conversation.language.name})
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
                    className={darkMode ? 'dark-mode' : ''}
                  >
                    <option value="">Select Language</option>
                    {languages.map((language) => (
                      <option key={language.id} value={language.id}>
                        {language.name}
                      </option>
                    ))}
                  </Form.Control>
                </Form.Group>
                <Form.Group controlId="newConversationTitle">
                  <Form.Control
                    type="text"
                    placeholder="Enter a title for the new conversation"
                    value={newConversationTitle}
                    onChange={(e) => setNewConversationTitle(e.target.value)}
                    required
                    className={darkMode ? 'dark-mode' : ''}
                  />
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
            <Card className={`chat-card ${darkMode ? 'dark-mode' : ''}`}>
              <Card.Header>
                <h4>
                  {selectedConversation.title} ({selectedConversation.language.name})
                </h4>
              </Card.Header>
              <Card.Body>
                <div className={`messages-container ${darkMode ? 'dark-mode' : ''}`}>
                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`message ${message.sender === 'user' ? 'user-message' : 'ai-message'} ${
                        darkMode ? 'dark-mode' : ''
                      }`}
                    >
                      <strong>{message.sender === 'user' ? 'You' : 'AI Teacher'}:</strong>
                      <div className="message-content">{renderMarkdown(message.content)}</div>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
                <Form onSubmit={handleSendMessage}>
                  <Form.Group controlId="newMessage" className={`mb-3 ${darkMode ? 'dark-mode' : ''}`}>
                    <Form.Control
                      as="textarea"
                      rows={3}
                      placeholder="Type your message..."
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      required
                      className={`${darkMode ? 'dark-mode' : ''}`}
                    />
                  </Form.Group>
                  <Button variant={darkMode ? 'light' : 'primary'} type="submit" disabled={isLoading}>
                    {isLoading ? 'Sending...' : 'Send'}
                  </Button>
                </Form>
              </Card.Body>
            </Card>
          ) : (
            <Card className={`chat-card ${darkMode ? 'dark-mode' : ''}`}>
              <Card.Body>
                <h4>Select a conversation to start chatting.</h4>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
      <Button
        variant={darkMode ? 'light' : 'dark'}
        onClick={toggleDarkMode}
        className="dark-mode-toggle"
      >
        {darkMode ? 'Light Mode' : 'Dark Mode'}
      </Button>
    </Container>
  );
}

export default Chat;