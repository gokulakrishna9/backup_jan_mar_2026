import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllJobPostQuestion } from '../../../store/slices/jobPostQuestionSlice';

const JobPostQuestionFilterPanel = () => {
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
    dispatch(fetchAllJobPostQuestion({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllJobPostQuestion({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter JobPostQuestion</h3>
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
        <label>Question Text</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.questionText || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('questionText', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.questionText || ''} onChange={(e) => handleFilterChange('questionText', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Question Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.questionType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('questionType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.questionType || ''} onChange={(e) => handleFilterChange('questionType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Required</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isRequired || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isRequired', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isRequired} onChange={(e) => handleFilterChange('isRequired', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Order Sequence</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.orderSequence || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('orderSequence', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.orderSequence} onValueChange={(e) => handleFilterChange('orderSequence', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default JobPostQuestionFilterPanel;