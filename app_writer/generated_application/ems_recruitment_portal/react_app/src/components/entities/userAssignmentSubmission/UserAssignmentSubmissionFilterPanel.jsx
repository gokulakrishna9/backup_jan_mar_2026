import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllUserAssignmentSubmission } from '../../../store/slices/userAssignmentSubmissionSlice';

const UserAssignmentSubmissionFilterPanel = () => {
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
    dispatch(fetchAllUserAssignmentSubmission({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllUserAssignmentSubmission({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter UserAssignmentSubmission</h3>
      <div className="field p-mb-3">
        <label>Submission Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.submissionId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('submissionId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.submissionId} onValueChange={(e) => handleFilterChange('submissionId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Assignment Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.assignmentId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('assignmentId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.assignmentId} onValueChange={(e) => handleFilterChange('assignmentId', e.value)} />
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
        <label>Submission Content</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.submissionContent || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('submissionContent', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.submissionContent || ''} onChange={(e) => handleFilterChange('submissionContent', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Submission File Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.submissionFileId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('submissionFileId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.submissionFileId} onValueChange={(e) => handleFilterChange('submissionFileId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Submitted At</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.submittedAt || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('submittedAt', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.submittedAt} onChange={(e) => handleFilterChange('submittedAt', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Score</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.score || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('score', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.score} onValueChange={(e) => handleFilterChange('score', e.value)} />
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
        <label>Graded By User Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.gradedByUserId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('gradedByUserId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.gradedByUserId} onValueChange={(e) => handleFilterChange('gradedByUserId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Graded At</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.gradedAt || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('gradedAt', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.gradedAt} onChange={(e) => handleFilterChange('gradedAt', e.value)} />
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
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default UserAssignmentSubmissionFilterPanel;