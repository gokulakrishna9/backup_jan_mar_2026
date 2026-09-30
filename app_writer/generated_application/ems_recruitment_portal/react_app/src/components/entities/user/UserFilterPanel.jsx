import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllUser } from '../../../store/slices/userSlice';

const UserFilterPanel = () => {
  const dispatch = useDispatch();
  const [filters, setFilters] = useState({});
  const [operators, setOperators] = useState({});

  const handleFilterChange = (field, value) => {
    setFilters((prev) => ({ ...prev, [field]: value }));
  };

  const handleOperatorChange = (field, value) => {
    setOperators((prev) => ({ ...prev, [field]: value }));
  };

  const handleApply = () => {
    const filterParams = {};
    Object.entries(filters).forEach(([field, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        const op = operators[field] || 'EQUALS';
        filterParams[`${field}_${op.toLowerCase()}`] = value;
      }
    });
    dispatch(fetchAllUser({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllUser({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter User</h3>
      <div className="field p-mb-3">
        <label>User Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.userId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('userId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.userId} onValueChange={(e) => handleFilterChange('userId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>First Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.firstName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('firstName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.firstName || ''} onChange={(e) => handleFilterChange('firstName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Last Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.lastName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('lastName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.lastName || ''} onChange={(e) => handleFilterChange('lastName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Gender</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.gender || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('gender', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.gender || ''} onChange={(e) => handleFilterChange('gender', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Date Of Birth</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.dateOfBirth || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('dateOfBirth', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.dateOfBirth} onChange={(e) => handleFilterChange('dateOfBirth', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Email Address</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.emailAddress || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('emailAddress', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.emailAddress || ''} onChange={(e) => handleFilterChange('emailAddress', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>User Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.userName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('userName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.userName || ''} onChange={(e) => handleFilterChange('userName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Encrypted Password</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.encryptedPassword || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('encryptedPassword', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.encryptedPassword || ''} onChange={(e) => handleFilterChange('encryptedPassword', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Phone Number</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.phoneNumber || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('phoneNumber', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.phoneNumber || ''} onChange={(e) => handleFilterChange('phoneNumber', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Profile Photo</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.profilePhoto || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('profilePhoto', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.profilePhoto || ''} onChange={(e) => handleFilterChange('profilePhoto', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Active</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isActive || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isActive', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isActive} onChange={(e) => handleFilterChange('isActive', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Entity</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isEntity || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isEntity', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isEntity} onChange={(e) => handleFilterChange('isEntity', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Public</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isPublic || 'equals'}
            options={ ["equals"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isPublic', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isPublic} onChange={(e) => handleFilterChange('isPublic', e.checked)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default UserFilterPanel;