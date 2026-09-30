import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllUserLanguage } from '../../../store/slices/userLanguageSlice';

const UserLanguageFilterPanel = () => {
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
    dispatch(fetchAllUserLanguage({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllUserLanguage({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter UserLanguage</h3>
      <div className="field p-mb-3">
        <label>Language Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.languageId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('languageId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.languageId} onValueChange={(e) => handleFilterChange('languageId', e.value)} />
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
        <label>Language Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.languageName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('languageName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.languageName || ''} onChange={(e) => handleFilterChange('languageName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Proficiency Level</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.proficiencyLevel || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('proficiencyLevel', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.proficiencyLevel || ''} onChange={(e) => handleFilterChange('proficiencyLevel', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Can Read</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.canRead || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('canRead', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.canRead} onChange={(e) => handleFilterChange('canRead', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Can Write</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.canWrite || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('canWrite', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.canWrite} onChange={(e) => handleFilterChange('canWrite', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Can Speak</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.canSpeak || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('canSpeak', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.canSpeak} onChange={(e) => handleFilterChange('canSpeak', e.checked)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default UserLanguageFilterPanel;