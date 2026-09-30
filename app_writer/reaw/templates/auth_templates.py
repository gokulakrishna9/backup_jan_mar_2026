"""Jinja2 templates for authentication components."""

LOGIN_PAGE = """import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';
import { useAuth } from './AuthContext';
import apiClient from '../services/apiClient';

const LoginPage = () => {
  const navigate = useNavigate();
  const toast = useRef(null);
  const { setAuth } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    try {
      const response = await apiClient.post('{{ loginEndpoint }}', { username, password });
      const { token, refreshToken, userId, username: uname, email, isSuperUser } = response.data;
      const user = response.data.user || { userId, username: uname, email, isSuperUser };
      setAuth({ token, refreshToken: refreshToken || null, user });
      navigate('/');
    } catch (err) {
      toast.current?.show({ severity: 'error', summary: 'Login Failed', detail: err.response?.data?.message || 'Invalid credentials', life: 5000 });
    }
    setLoading(false);
  };

  return (
    <div className="p-d-flex p-jc-center p-ai-center" style={ { minHeight: '100vh' } }>
      <Toast ref={toast} />
      <div className="p-card p-p-4" style={ { width: '400px' } }>
        <h2>Login</h2>
        <div className="field p-mb-3">
          <label htmlFor="username">Username</label>
          <InputText id="username" value={username} onChange={(e) => setUsername(e.target.value)} className="p-d-block" style={ { width: '100%' } } />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="password">Password</label>
          <InputText id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="p-d-block" style={ { width: '100%' } } />
        </div>
        <Button label="Login" icon="pi pi-sign-in" loading={loading} onClick={handleLogin} className="p-mb-2" style={ { width: '100%' } } />
{% if oauth2Enabled %}{% for provider in oauth2Providers %}        <Button label="Login with {{ provider }}" icon="pi pi-external-link" className="p-button-outlined p-mb-2" style={ { width: '100%' } } onClick={() => window.location.href = '{{ loginEndpoint | replace("/login", "/oauth2/") }}{{ provider | lower }}'} />
{% endfor %}{% endif %}{% if registerEnabled %}        <div className="p-mt-3 p-text-center">
          <a href="/register">Don't have an account? Register</a>
        </div>
{% endif %}      </div>
    </div>
  );
};

export default LoginPage;
"""

REGISTER_PAGE = """import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';
import apiClient from '../services/apiClient';

const RegisterPage = () => {
  const navigate = useNavigate();
  const toast = useRef(null);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleRegister = async () => {
    setLoading(true);
    try {
      await apiClient.post('{{ registerEndpoint }}', formData);
      toast.current?.show({ severity: 'success', summary: 'Registered', detail: 'Account created. Please login.', life: 3000 });
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      toast.current?.show({ severity: 'error', summary: 'Registration Failed', detail: err.response?.data?.message || 'Error', life: 5000 });
    }
    setLoading(false);
  };

  return (
    <div className="p-d-flex p-jc-center p-ai-center" style={ { minHeight: '100vh' } }>
      <Toast ref={toast} />
      <div className="p-card p-p-4" style={ { width: '500px' } }>
        <h2>Register</h2>
{% for field in userEntityInputFields %}        <div className="field p-mb-3">
          <label htmlFor="{{ field.fieldName }}">{{ field.fieldLabel }}</label>
{% if field.componentType == 'InputText' %}          <InputText id="{{ field.fieldName }}" value={formData.{{ field.fieldName }} || ''} onChange={(e) => handleChange('{{ field.fieldName }}', e.target.value)} style={ { width: '100%' } } />
{% elif field.componentType == 'InputNumber' %}          <InputNumber id="{{ field.fieldName }}" value={formData.{{ field.fieldName }}} onValueChange={(e) => handleChange('{{ field.fieldName }}', e.value)} style={ { width: '100%' } } />
{% elif field.componentType == 'Calendar' %}          <Calendar id="{{ field.fieldName }}" value={formData.{{ field.fieldName }}} onChange={(e) => handleChange('{{ field.fieldName }}', e.value)} style={ { width: '100%' } } />
{% elif field.componentType == 'Checkbox' %}          <Checkbox id="{{ field.fieldName }}" checked={!!formData.{{ field.fieldName }}} onChange={(e) => handleChange('{{ field.fieldName }}', e.checked)} />
{% else %}          <InputText id="{{ field.fieldName }}" value={formData.{{ field.fieldName }} || ''} onChange={(e) => handleChange('{{ field.fieldName }}', e.target.value)} style={ { width: '100%' } } />
{% endif %}        </div>
{% endfor %}        <Button label="Register" icon="pi pi-user-plus" loading={loading} onClick={handleRegister} style={ { width: '100%' } } />
        <div className="p-mt-3 p-text-center">
          <a href="/login">Already have an account? Login</a>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
"""

AUTH_CONTEXT = """import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
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
      const response = await apiClient.get('{{ permissionsEndpoint }}');
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
"""

PROTECTED_ROUTE = """import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
"""
