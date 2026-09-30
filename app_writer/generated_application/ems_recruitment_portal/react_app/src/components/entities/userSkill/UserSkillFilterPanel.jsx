import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllUserSkill } from '../../../store/slices/userSkillSlice';

const UserSkillFilterPanel = () => {
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
    dispatch(fetchAllUserSkill({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllUserSkill({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter UserSkill</h3>
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
        <label>Skill Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.skillName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('skillName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.skillName || ''} onChange={(e) => handleFilterChange('skillName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Skill Category</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.skillCategory || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('skillCategory', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.skillCategory || ''} onChange={(e) => handleFilterChange('skillCategory', e.target.value)} />
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
        <label>Years Of Experience</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.yearsOfExperience || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('yearsOfExperience', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.yearsOfExperience} onValueChange={(e) => handleFilterChange('yearsOfExperience', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Verified</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isVerified || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isVerified', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isVerified} onChange={(e) => handleFilterChange('isVerified', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Verified By Institution Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.verifiedByInstitutionId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('verifiedByInstitutionId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.verifiedByInstitutionId} onValueChange={(e) => handleFilterChange('verifiedByInstitutionId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Endorsement Count</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.endorsementCount || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('endorsementCount', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.endorsementCount} onValueChange={(e) => handleFilterChange('endorsementCount', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default UserSkillFilterPanel;