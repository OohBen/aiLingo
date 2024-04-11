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
  const [darkMode, setDarkMode] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchConversations();
    fetchLanguages();
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

  const handleConversationClick = (conversation) => {
    setSelectedConversation(conversation);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault(); // Add this line to prevent form submission
    if (isLoading || !newMessage.trim()) return;
  
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
    if (!newConversationTitle.trim() || !newConversationLanguage) return;

    try {
      const selectedLanguage = languages.find((lang) => lang.id === parseInt(newConversationLanguage));

      const response = await axiosInstance.post('/chat/conversations/', {
        language: selectedLanguage,
        title: newConversationTitle,
      });

      setConversations([...conversations, response.data]);
      setSelectedConversation(response.data);
      setNewConversationLanguage('');
      setNewConversationTitle('');
    } catch (error) {
      console.error('Error creating new conversation:', error);
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };
  const renderMarkdown = (message) => {
    if (message.content.includes('Quiz created successfully!')) {
        const quizLink = message.content.match(/(\/quizzes\/\d+)/)[0];
        return (
            <div className="quiz-creation-message">
                A new quiz has been created! <br />
                <a href={quizLink}>Start the quiz</a>
            </div>
        );
    } else {
        return <Markdown remarkPlugins={[remarkGfm]}>{message.content}</Markdown>;
    }
}


  return (
    <Container fluid className={`chat-container ${darkMode ? 'dark-mode' : ''}`}>
      <Row>
        <Col md={4} className="sidebar-scroll">
          <Card className={`conversations-card ${darkMode ? 'dark-mode' : ''}`}>
            <Card.Header>
              <h4>Conversations</h4>
            </Card.Header>
            <Card.Body>
              <ul className="list-unstyled">
                {conversations.map((conversation) => (
                  <li
                    key={conversation.id}
                    className={`conversation-item ${conversation === selectedConversation ? 'active' : ''}`}
                    onClick={() => handleConversationClick(conversation)}
                  >
                    {conversation.title} ({conversation.language.name})
                  </li>
                ))}
              </ul>
              <Form onSubmit={handleNewConversation}>
                <Form.Group controlId="newConversationLanguage">
                  <Form.Label>Language</Form.Label>
                  <Form.Control
                    as="select"
                    value={newConversationLanguage}
                    onChange={(e) => setNewConversationLanguage(e.target.value)}
                    required
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
                  <Form.Label>Title</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Enter conversation title"
                    value={newConversationTitle}
                    onChange={(e) => setNewConversationTitle(e.target.value)}
                    required
                  />
                </Form.Group>
                <Button variant="primary" type="submit" className="mt-3">
                  Create Conversation
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
        <Col md={8}>
          {selectedConversation ? (
            <Card className={`chat-card ${darkMode ? 'dark-mode' : ''}`}>
              <Card.Header>
                <h4>{selectedConversation.title}</h4>
              </Card.Header>
              <Card.Body>
                <div className="messages-container">
                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`message ${message.sender === 'user' ? 'user-message' : 'ai-message'}`}>
                      <strong>{message.sender === 'user' ? 'You' : 'AI Teacher'}:</strong>
                      <div className="message-content">{renderMarkdown(message)}</div>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
                <Form onSubmit={handleSendMessage}>
  <Form.Group controlId="newMessage">
    <Form.Label>Message</Form.Label>
    <Form.Control
      as="textarea"
      rows={3}
      placeholder="Type your message (Enter to send, Shift+Enter for new line)..."
      value={newMessage}
      onChange={(e) => setNewMessage(e.target.value)}
      required
    />
  </Form.Group>
  <Button variant="primary" type="submit" disabled={isLoading} className="mt-3">
    {isLoading ? 'Sending...' : 'Send'}
  </Button>
</Form>              </Card.Body>
            </Card>
          ) : (<Card className={`chat-card ${darkMode ? 'dark-mode' : ''}`}>
            <Card.Body>
              <h4>Select a conversation to start chatting.</h4>
            </Card.Body>
          </Card>
          )}
        </Col>
      </Row>
      <Button variant={darkMode ? 'light' : 'dark'} onClick={toggleDarkMode} className="mt-3">
        {darkMode ? 'Light Mode' : 'Dark Mode'}
      </Button>
    </Container>
  );
}

export default Chat;

