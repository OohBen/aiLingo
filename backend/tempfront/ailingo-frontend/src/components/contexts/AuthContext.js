// src/components/contexts/AuthContext.js
import React, { createContext, useContext, useEffect, useState } from 'react';
import { isLoggedIn, logoutUser } from '../../utils/auth';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));

  useEffect(() => {
    const checkAuthStatus = () => {
      setLoggedIn(isLoggedIn());
      setUser(JSON.parse(localStorage.getItem('user')));
    };

    window.addEventListener('storage', checkAuthStatus);

    return () => {
      window.removeEventListener('storage', checkAuthStatus);
    };
  }, []);

  const logout = () => {
    logoutUser();
    setLoggedIn(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ loggedIn, user, setLoggedIn, logout }}>
      {children}
    </AuthContext.Provider>
  );
};