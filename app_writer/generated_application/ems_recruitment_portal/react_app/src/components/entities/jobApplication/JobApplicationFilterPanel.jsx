import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllJobApplication } from '../../../store/slices/jobApplicationSlice';

const JobApplicationFilterPanel = () => {
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
    dispatch(fetchAllJobApplication({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllJobApplication({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter JobApplication</h3>
      <div className="field p-mb-3">
        <label>Application Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.applicationId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('applicationId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.applicationId} onValueChange={(e) => handleFilterChange('applicationId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Job Post Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.jobPostId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('jobPostId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.jobPostId} onValueChange={(e) => handleFilterChange('jobPostId', e.value)} />
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
        <label>Cover Letter</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.coverLetter || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('coverLetter', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.coverLetter || ''} onChange={(e) => handleFilterChange('coverLetter', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Resume Document Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.resumeDocumentId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('resumeDocumentId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.resumeDocumentId} onValueChange={(e) => handleFilterChange('resumeDocumentId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Application Status</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.applicationStatus || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('applicationStatus', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.applicationStatus || ''} onChange={(e) => handleFilterChange('applicationStatus', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Applied At</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.appliedAt || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('appliedAt', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.appliedAt} onChange={(e) => handleFilterChange('appliedAt', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Status Updated At</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.statusUpdatedAt || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('statusUpdatedAt', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.statusUpdatedAt} onChange={(e) => handleFilterChange('statusUpdatedAt', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Status Updated By User Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.statusUpdatedByUserId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('statusUpdatedByUserId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.statusUpdatedByUserId} onValueChange={(e) => handleFilterChange('statusUpdatedByUserId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Notes</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.notes || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('notes', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.notes || ''} onChange={(e) => handleFilterChange('notes', e.target.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default JobApplicationFilterPanel;