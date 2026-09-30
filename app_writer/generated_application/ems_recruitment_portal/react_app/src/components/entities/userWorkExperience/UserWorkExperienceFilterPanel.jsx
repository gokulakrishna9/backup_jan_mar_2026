import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllUserWorkExperience } from '../../../store/slices/userWorkExperienceSlice';

const UserWorkExperienceFilterPanel = () => {
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
    dispatch(fetchAllUserWorkExperience({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllUserWorkExperience({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter UserWorkExperience</h3>
      <div className="field p-mb-3">
        <label>Experience Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.experienceId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('experienceId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.experienceId} onValueChange={(e) => handleFilterChange('experienceId', e.value)} />
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
        <label>Job Title</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.jobTitle || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('jobTitle', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.jobTitle || ''} onChange={(e) => handleFilterChange('jobTitle', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Company Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.companyName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('companyName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.companyName || ''} onChange={(e) => handleFilterChange('companyName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Employment Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.employmentType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('employmentType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.employmentType || ''} onChange={(e) => handleFilterChange('employmentType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Location</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.location || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('location', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.location || ''} onChange={(e) => handleFilterChange('location', e.target.value)} />
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
        <label>Is Current</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isCurrent || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isCurrent', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isCurrent} onChange={(e) => handleFilterChange('isCurrent', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Responsibilities</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.responsibilities || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('responsibilities', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.responsibilities || ''} onChange={(e) => handleFilterChange('responsibilities', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Achievements</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.achievements || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('achievements', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.achievements || ''} onChange={(e) => handleFilterChange('achievements', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Skills Used</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.skillsUsed || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('skillsUsed', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.skillsUsed || ''} onChange={(e) => handleFilterChange('skillsUsed', e.target.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default UserWorkExperienceFilterPanel;