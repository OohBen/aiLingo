import React from 'react';
import { Route, Navigate } from 'react-router-dom';

const PrivateRoute = ({ element: Component, ...rest }) => {
    const isAuthenticated = !!localStorage.getItem('access_token');

    return (
        <Route
            {...rest}
            element={isAuthenticated ? <Component {...rest} /> : <Navigate to="/login" />}
        />
    );
};

export default PrivateRoute;