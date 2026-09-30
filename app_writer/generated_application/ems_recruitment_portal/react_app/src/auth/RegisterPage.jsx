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
        <div className="field p-mb-3">
          <label htmlFor="firstName">First Name</label>
          <InputText id="firstName" value={formData.firstName || ''} onChange={(e) => handleChange('firstName', e.target.value)} style={ { width: '100%' } } />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="lastName">Last Name</label>
          <InputText id="lastName" value={formData.lastName || ''} onChange={(e) => handleChange('lastName', e.target.value)} style={ { width: '100%' } } />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="gender">Gender</label>
          <InputText id="gender" value={formData.gender || ''} onChange={(e) => handleChange('gender', e.target.value)} style={ { width: '100%' } } />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="dateOfBirth">Date Of Birth</label>
          <Calendar id="dateOfBirth" value={formData.dateOfBirth} onChange={(e) => handleChange('dateOfBirth', e.value)} style={ { width: '100%' } } />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="emailAddress">Email Address</label>
          <InputText id="emailAddress" value={formData.emailAddress || ''} onChange={(e) => handleChange('emailAddress', e.target.value)} style={ { width: '100%' } } />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="userName">User Name</label>
          <InputText id="userName" value={formData.userName || ''} onChange={(e) => handleChange('userName', e.target.value)} style={ { width: '100%' } } />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="encryptedPassword">Encrypted Password</label>
          <InputText id="encryptedPassword" value={formData.encryptedPassword || ''} onChange={(e) => handleChange('encryptedPassword', e.target.value)} style={ { width: '100%' } } />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="phoneNumber">Phone Number</label>
          <InputText id="phoneNumber" value={formData.phoneNumber || ''} onChange={(e) => handleChange('phoneNumber', e.target.value)} style={ { width: '100%' } } />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="profilePhoto">Profile Photo</label>
          <InputText id="profilePhoto" value={formData.profilePhoto || ''} onChange={(e) => handleChange('profilePhoto', e.target.value)} style={ { width: '100%' } } />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="isActive">Is Active</label>
          <Checkbox id="isActive" checked={!!formData.isActive} onChange={(e) => handleChange('isActive', e.checked)} />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="isEntity">Is Entity</label>
          <Checkbox id="isEntity" checked={!!formData.isEntity} onChange={(e) => handleChange('isEntity', e.checked)} />
        </div>
        <div className="field p-mb-3">
          <label htmlFor="isPublic">Is Public</label>
          <Checkbox id="isPublic" checked={!!formData.isPublic} onChange={(e) => handleChange('isPublic', e.checked)} />
        </div>
        <Button label="Register" icon="pi pi-user-plus" loading={loading} onClick={handleRegister} style={ { width: '100%' } } />
        <div className="p-mt-3 p-text-center">
          <a href="/login">Already have an account? Login</a>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;