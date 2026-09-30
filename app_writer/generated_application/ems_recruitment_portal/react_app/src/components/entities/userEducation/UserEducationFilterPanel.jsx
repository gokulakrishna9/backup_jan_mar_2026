import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllUserEducation } from '../../../store/slices/userEducationSlice';

const UserEducationFilterPanel = () => {
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
    dispatch(fetchAllUserEducation({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllUserEducation({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter UserEducation</h3>
      <div className="field p-mb-3">
        <label>Education Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.educationId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('educationId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.educationId} onValueChange={(e) => handleFilterChange('educationId', e.value)} />
        </div>
      </div>
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
        <label>Institution Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.institutionId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('institutionId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.institutionId} onValueChange={(e) => handleFilterChange('institutionId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Degree Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.degreeType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('degreeType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.degreeType || ''} onChange={(e) => handleFilterChange('degreeType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Field Of Study</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.fieldOfStudy || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('fieldOfStudy', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.fieldOfStudy || ''} onChange={(e) => handleFilterChange('fieldOfStudy', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Specialization</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.specialization || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('specialization', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.specialization || ''} onChange={(e) => handleFilterChange('specialization', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Start Date</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.startDate || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('startDate', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.startDate} onChange={(e) => handleFilterChange('startDate', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>End Date</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.endDate || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('endDate', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.endDate} onChange={(e) => handleFilterChange('endDate', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Grade Gpa</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.gradeGpa || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('gradeGpa', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.gradeGpa || ''} onChange={(e) => handleFilterChange('gradeGpa', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Verified</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isVerified || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isVerified', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isVerified} onChange={(e) => handleFilterChange('isVerified', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Certificate Document Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.certificateDocumentId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('certificateDocumentId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.certificateDocumentId} onValueChange={(e) => handleFilterChange('certificateDocumentId', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default UserEducationFilterPanel;