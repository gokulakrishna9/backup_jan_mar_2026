import React, { useState, useRef } from 'react';
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
      const response = await apiClient.post('/api/auth/login', { username, password });
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
        <div className="p-mt-3 p-text-center">
          <a href="/register">Don't have an account? Register</a>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;