import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllUserSkillEndorsement } from '../../../store/slices/userSkillEndorsementSlice';

const UserSkillEndorsementFilterPanel = () => {
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
    dispatch(fetchAllUserSkillEndorsement({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllUserSkillEndorsement({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter UserSkillEndorsement</h3>
      <div className="field p-mb-3">
        <label>Endorsement Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.endorsementId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('endorsementId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.endorsementId} onValueChange={(e) => handleFilterChange('endorsementId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Skill Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.skillId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('skillId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.skillId} onValueChange={(e) => handleFilterChange('skillId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Endorsed By User Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.endorsedByUserId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('endorsedByUserId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.endorsedByUserId} onValueChange={(e) => handleFilterChange('endorsedByUserId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Endorsement Comment</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.endorsementComment || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('endorsementComment', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.endorsementComment || ''} onChange={(e) => handleFilterChange('endorsementComment', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Relationship</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.relationship || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('relationship', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.relationship || ''} onChange={(e) => handleFilterChange('relationship', e.target.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default UserSkillEndorsementFilterPanel;