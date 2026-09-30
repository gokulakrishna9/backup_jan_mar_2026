import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllAiCommunityPostEvaluation } from '../../../store/slices/aiCommunityPostEvaluationSlice';

const AiCommunityPostEvaluationFilterPanel = () => {
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
    dispatch(fetchAllAiCommunityPostEvaluation({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllAiCommunityPostEvaluation({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter AiCommunityPostEvaluation</h3>
      <div className="field p-mb-3">
        <label>Evaluation Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.evaluationId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('evaluationId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.evaluationId} onValueChange={(e) => handleFilterChange('evaluationId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Post Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.postId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('postId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.postId} onValueChange={(e) => handleFilterChange('postId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Evaluation Summary</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.evaluationSummary || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('evaluationSummary', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.evaluationSummary || ''} onChange={(e) => handleFilterChange('evaluationSummary', e.target.value)} />
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

export default AiCommunityPostEvaluationFilterPanel;