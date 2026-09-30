import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../services/apiClient';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [refreshToken, setRefreshToken] = useState(() => localStorage.getItem('refreshToken'));
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('user');
    return stored ? JSON.parse(stored) : null;
  });
  const [allowedApiList, setAllowedApiList] = useState(() => {
    const stored = localStorage.getItem('allowedApiList');
    return stored ? JSON.parse(stored) : [];
  });

  const isAuthenticated = !!token;

  const setAuth = useCallback(({ token: t, refreshToken: rt, user: u }) => {
    setToken(t);
    setRefreshToken(rt);
    setUser(u);
    localStorage.setItem('token', t);
    if (rt) localStorage.setItem('refreshToken', rt);
    if (u) localStorage.setItem('user', JSON.stringify(u));
  }, []);

  const logout = useCallback(() => {
    setToken(null);
    setRefreshToken(null);
    setUser(null);
    setAllowedApiList([]);
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    localStorage.removeItem('allowedApiList');
    navigate('/login');
  }, [navigate]);

  const fetchPermissions = useCallback(async () => {
    try {
      const response = await apiClient.get('/api/auth/permissions');
      const permissions = response.data || [];
      setAllowedApiList(permissions);
      localStorage.setItem('allowedApiList', JSON.stringify(permissions));
    } catch (err) {
      console.error('Failed to fetch permissions:', err);
    }
  }, []);

  useEffect(() => {
    if (token) {
      fetchPermissions();
    }
  }, [token, fetchPermissions]);

  return (
    <AuthContext.Provider value={ { token, refreshToken, user, isAuthenticated, allowedApiList, setAuth, logout, fetchPermissions } }>
      {children}
    </AuthContext.Provider>
  );
};