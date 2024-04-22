// src/components/ChatInterface.tsx
'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { createConversation, sendMessage, getConversations, getMessages, getLanguages } from '../lib/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export function ChatInterface() {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [languages, setLanguages] = useState([]);
  const [newConversationLanguage, setNewConversationLanguage] = useState('');
  const [newConversationTitle, setNewConversationTitle] = useState('');
  const [isSending, setIsSending] = useState(false);

  const router = useRouter();
  const chatContainerRef = useRef(null);

  useEffect(() => {
    fetchConversations();
    fetchLanguages();
  }, []);

  useEffect(() => {
    if (selectedConversation) {
      fetchMessages();
    }
  }, [selectedConversation]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchConversations = async () => {
    try {
      const data = await getConversations();
      setConversations(data);
    } catch (error) {
      console.error('Failed to fetch conversations:', error);
    }
  };

  const fetchLanguages = async () => {
    try {
      const data = await getLanguages();
      setLanguages(data);
    } catch (error) {
      console.error('Failed to fetch languages:', error);
    }
  };

  const fetchMessages = async () => {
    try {
      const data = await getMessages(selectedConversation.id);
      setMessages(data);
    } catch (error) {
      console.error('Failed to fetch messages:', error);
    }
  };

  const handleConversationClick = (conversation) => {
    setSelectedConversation(conversation);
  };

  const handleSendMessage = async () => {
    if (inputMessage.trim() !== '' && !isSending) {
      setIsSending(true);
      try {
        const newMessage = {
          id: Date.now().toString(),
          conversation: selectedConversation.id,
          sender: 'user',
          content: inputMessage,
          timestamp: new Date().toISOString(),
        };

        setMessages((prevMessages) => [...prevMessages, newMessage]);
        setInputMessage('');

        const data = await sendMessage(selectedConversation.id, inputMessage);
        setMessages((prevMessages) => [...prevMessages, data]);
      } catch (error) {
        console.error('Failed to send message:', error);
      }

      setIsSending(false);
    }
  };

  const handleCreateConversation = async () => {
    if (newConversationLanguage && newConversationTitle) {
      try {
        const data = await createConversation(newConversationLanguage, newConversationTitle);
        setConversations([...conversations, data]);
        setSelectedConversation(data);
        setNewConversationLanguage('');
        setNewConversationTitle('');
      } catch (error) {
        console.error('Failed to create conversation:', error);
      }
    }
  };

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  return (
    <div className="flex">
      <div className="w-1/4 bg-gray-200 p-4">
        <h2 className="text-xl font-semibold mb-4">Conversations</h2>
        <ul>
          {conversations.map((conversation) => (
            <li
              key={conversation.id}
              className={`cursor-pointer mb-2 ${selectedConversation?.id === conversation.id ? 'font-bold' : ''
                }`}
              onClick={() => handleConversationClick(conversation)}
            >
              {conversation.title}
            </li>
          ))}
        </ul>
        <div className="mt-4">
          <h3 className="text-lg font-semibold mb-2">New Conversation</h3>
          <select
            className="block w-full mb-2"
            value={newConversationLanguage}
            onChange={(e) => setNewConversationLanguage(e.target.value)}
          >
            <option value="">Select Language</option>
            {languages.map((language) => (
              <option key={language.id} value={language.id}>
                {language.name}
              </option>
            ))}
          </select>
          <input
            type="text"
            className="block w-full mb-2"
            placeholder="Conversation Title"
            value={newConversationTitle}
            onChange={(e) => setNewConversationTitle(e.target.value)}
          />
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded-lg"
            onClick={handleCreateConversation}
          >
            Create Conversation
          </button>
        </div>
      </div>
      <div className="w-3/4 bg-white shadow-md rounded-lg p-4">
        <h2 className="text-xl font-semibold mb-4">
          {selectedConversation?.title || 'Select a conversation'}
        </h2>
        <div ref={chatContainerRef} className="h-64 overflow-y-auto mb-4">
  {messages.map((message) => (
    <div
      key={message.id}
      className={`mb-2 ${
        message.sender === 'user' ? 'text-right' : 'text-left'
      }`}
    >
      <span
        className={`inline-block px-3 py-2 rounded-lg ${
          message.sender === 'user'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-200 text-gray-800'
        }`}
      >
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            a: ({ node, ...props }) => (
              <a {...props} className="text-blue-500 hover:underline" />
            ),
          }}
        >
          {message.content.replace(/\\n/g, '\n')}
        </ReactMarkdown>
      </span>
    </div>
  ))}
</div>

        <div className="flex">
          <input
            type="text"
            className="flex-grow border border-gray-300 rounded-lg px-4 py-2 mr-2"
            placeholder="Type your message..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
          />
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded-lg"
            onClick={handleSendMessage}
            disabled={!selectedConversation || isSending}
          >
            {isSending ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}


