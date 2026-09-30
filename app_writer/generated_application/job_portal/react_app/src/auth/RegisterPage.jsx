import React, { useState, useRef } from 'react';
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
      await apiClient.post('/api/auth/register', formData);
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
        <Button label="Register" icon="pi pi-user-plus" loading={loading} onClick={handleRegister} style={ { width: '100%' } } />
        <div className="p-mt-3 p-text-center">
          <a href="/login">Already have an account? Login</a>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;