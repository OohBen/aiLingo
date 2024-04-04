import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
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
function App() {
  return (
    <Router>
      <div>
        <Navigation />
        <div className="container">
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/languages" element={<Languages />} />
            <Route path="/lessons" element={<Lessons />} />
            <Route path="/quizzes" element={<Quizzes />} />
            <Route path="/generate-question" element={<GenerateQuestion />} />
            <Route path="/create-quiz" element={<CreateQuiz />} />
            <Route path="/quizzes" element={<Quizzes />} />
            <Route path="/quizzes/:id" element={<QuizDetails />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;