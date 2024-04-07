// App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { useState } from 'react';
import { Container } from 'react-bootstrap';
import Navigation from './components/Navigation';
import Home from './components/Home';
import Register from './components/Register';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Languages from './components/Languages';
import Lessons from './components/Lessons';
import Quizzes from './components/Quizzes';
import QuizDetails from './components/QuizDetails';
import GenerateQuestion from './components/GenerateQuestion';
import CreateQuiz from './components/CreateQuiz';
import Profile from './components/Profile';
import QuizAttempt from './components/QuizAttempt';
import Chat from './components/Chat';
import Analytics from './components/Analytics';
import { AuthProvider } from './components/contexts/AuthContext';
function App() {
  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <AuthProvider>
      <Router>
        <div className={darkMode ? 'dark-mode' : ''}>
          <Navigation darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
          <Container>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/register" element={<Register />} />
              <Route path="/login" element={<Login />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/languages" element={<Languages />} />
              <Route path="/lessons" element={<Lessons />} />
              <Route path="/quizzes" element={<Quizzes />} />
              <Route path="/quizzes/:id" element={<QuizAttempt />} />
              <Route path="/generate-question" element={<GenerateQuestion />} />
              <Route path="/create-quiz" element={<CreateQuiz />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/chat" element={<Chat />} />
              <Route path="/analytics" element={<Analytics />} />
            </Routes>
          </Container>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;