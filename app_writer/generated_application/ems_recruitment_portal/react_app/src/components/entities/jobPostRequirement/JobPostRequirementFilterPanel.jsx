import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllJobPostRequirement } from '../../../store/slices/jobPostRequirementSlice';

const JobPostRequirementFilterPanel = () => {
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
    dispatch(fetchAllJobPostRequirement({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllJobPostRequirement({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter JobPostRequirement</h3>
      <div className="field p-mb-3">
        <label>Requirement Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.requirementId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('requirementId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.requirementId} onValueChange={(e) => handleFilterChange('requirementId', e.value)} />
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
        <label>Requirement Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.requirementType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('requirementType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.requirementType || ''} onChange={(e) => handleFilterChange('requirementType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Requirement Description</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.requirementDescription || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('requirementDescription', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.requirementDescription || ''} onChange={(e) => handleFilterChange('requirementDescription', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Mandatory</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isMandatory || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isMandatory', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isMandatory} onChange={(e) => handleFilterChange('isMandatory', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Minimum Years</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.minimumYears || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('minimumYears', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.minimumYears} onValueChange={(e) => handleFilterChange('minimumYears', e.value)} />
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
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default JobPostRequirementFilterPanel;