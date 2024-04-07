import React, { createContext, useContext, useEffect, useState } from 'react';
import { isLoggedIn, logoutUser } from '../../utils/auth';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());

  useEffect(() => {
    const checkAuthStatus = () => {
      setLoggedIn(isLoggedIn());
    };

    window.addEventListener('storage', checkAuthStatus);

    return () => {
      window.removeEventListener('storage', checkAuthStatus);
    };
  }, []);

  const logout = () => {
    logoutUser();
    setLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ loggedIn, setLoggedIn, logout }}>
      {children}
    </AuthContext.Provider>
  );
};