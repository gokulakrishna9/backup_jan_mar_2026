import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllAiUserProfileEvaluationParameter } from '../../../store/slices/aiUserProfileEvaluationParameterSlice';

const AiUserProfileEvaluationParameterFilterPanel = () => {
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
    dispatch(fetchAllAiUserProfileEvaluationParameter({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllAiUserProfileEvaluationParameter({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter AiUserProfileEvaluationParameter</h3>
      <div className="field p-mb-3">
        <label>Parameter Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.parameterId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('parameterId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.parameterId} onValueChange={(e) => handleFilterChange('parameterId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Parameter Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.parameterName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('parameterName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.parameterName || ''} onChange={(e) => handleFilterChange('parameterName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Group Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.groupId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('groupId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.groupId} onValueChange={(e) => handleFilterChange('groupId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Parameter Value</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.parameterValue || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('parameterValue', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.parameterValue || ''} onChange={(e) => handleFilterChange('parameterValue', e.target.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default AiUserProfileEvaluationParameterFilterPanel;