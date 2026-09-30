import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllJobApplicationAnswer } from '../../../store/slices/jobApplicationAnswerSlice';

const JobApplicationAnswerFilterPanel = () => {
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
    dispatch(fetchAllJobApplicationAnswer({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllJobApplicationAnswer({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter JobApplicationAnswer</h3>
      <div className="field p-mb-3">
        <label>Answer Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.answerId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('answerId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.answerId} onValueChange={(e) => handleFilterChange('answerId', e.value)} />
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
        <label>Question Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.questionId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('questionId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.questionId} onValueChange={(e) => handleFilterChange('questionId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Answer Text</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.answerText || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('answerText', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.answerText || ''} onChange={(e) => handleFilterChange('answerText', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Answer File Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.answerFileId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('answerFileId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.answerFileId} onValueChange={(e) => handleFilterChange('answerFileId', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default JobApplicationAnswerFilterPanel;