import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllJobInterview } from '../../../store/slices/jobInterviewSlice';

const JobInterviewFilterPanel = () => {
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
    dispatch(fetchAllJobInterview({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllJobInterview({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter JobInterview</h3>
      <div className="field p-mb-3">
        <label>Interview Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.interviewId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('interviewId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.interviewId} onValueChange={(e) => handleFilterChange('interviewId', e.value)} />
        </div>
      </div>
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
        <label>Interview Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.interviewType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('interviewType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.interviewType || ''} onChange={(e) => handleFilterChange('interviewType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Interview Round</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.interviewRound || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('interviewRound', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.interviewRound} onValueChange={(e) => handleFilterChange('interviewRound', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Scheduled At</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.scheduledAt || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('scheduledAt', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.scheduledAt} onChange={(e) => handleFilterChange('scheduledAt', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Duration Minutes</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.durationMinutes || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('durationMinutes', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.durationMinutes} onValueChange={(e) => handleFilterChange('durationMinutes', e.value)} />
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
        <label>Meeting Link</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.meetingLink || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('meetingLink', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.meetingLink || ''} onChange={(e) => handleFilterChange('meetingLink', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Interviewer User Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.interviewerUserId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('interviewerUserId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.interviewerUserId} onValueChange={(e) => handleFilterChange('interviewerUserId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Status</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.status || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('status', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.status || ''} onChange={(e) => handleFilterChange('status', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Feedback</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.feedback || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('feedback', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.feedback || ''} onChange={(e) => handleFilterChange('feedback', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Rating</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.rating || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('rating', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.rating} onValueChange={(e) => handleFilterChange('rating', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default JobInterviewFilterPanel;