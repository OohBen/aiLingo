// ConversationPage.js

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Row, Col, Card, Form, Button } from 'react-bootstrap';
import axiosInstance from '../utils/axiosInstance';
import ReactMarkdown from 'react-markdown';

function ConversationPage({ darkMode }) {
  const { id } = useParams();
  const [conversation, setConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    // fetchConversation();
    fetchMessages();
  }, [id]);

//   const fetchConversation = async () => {
//     try {
//       const response = await axiosInstance.get(`/chat/conversations/${id}/`);
//       setConversation(response.data);
//     } catch (error) {
//       console.error('Error fetching conversation:', error);
//     }
//   };

  const fetchMessages = async () => {
    try {
      const response = await axiosInstance.get(`/chat/conversations/${id}/messages/`);
      setMessages(response.data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post(`/chat/conversations/${id}/messages/`, {
        content: newMessage,
      });
      setMessages([...messages, response.data]);
      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  if (!conversation) {
    return <div>Loading...</div>;
  }

  return (
    <Container className={darkMode ? 'dark-mode' : ''}>
      <Row>
        <Col>
          <h2>{conversation.language.name} Conversation</h2>
          <Card className={`mb-3 ${darkMode ? 'bg-dark text-light' : ''}`}>
            <Card.Body>
              <div className="chat-messages">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`message ${
                      message.sender === 'user' ? 'user-message' : 'ai-message'
                    } ${darkMode ? 'bg-secondary text-light' : ''}`}
                  >
                    <strong>{message.sender === 'user' ? 'You' : 'AI Teacher'}:</strong>
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                  </div>
                ))}
              </div>
              <Form onSubmit={handleSendMessage}>
                <Form.Group controlId="newMessage">
                  <Form.Control
                    as="textarea"
                    rows={3}
                    placeholder="Type your message..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    required
                    className={darkMode ? 'bg-dark text-light' : ''}
                  />
                </Form.Group>
                <Button variant={darkMode ? 'light' : 'primary'} type="submit">
                  Send
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default ConversationPage;