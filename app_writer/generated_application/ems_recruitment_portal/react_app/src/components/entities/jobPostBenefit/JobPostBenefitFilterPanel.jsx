import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllJobPostBenefit } from '../../../store/slices/jobPostBenefitSlice';

const JobPostBenefitFilterPanel = () => {
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
    dispatch(fetchAllJobPostBenefit({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllJobPostBenefit({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter JobPostBenefit</h3>
      <div className="field p-mb-3">
        <label>Benefit Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.benefitId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('benefitId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.benefitId} onValueChange={(e) => handleFilterChange('benefitId', e.value)} />
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
        <label>Benefit Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.benefitType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('benefitType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.benefitType || ''} onChange={(e) => handleFilterChange('benefitType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Benefit Description</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.benefitDescription || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('benefitDescription', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.benefitDescription || ''} onChange={(e) => handleFilterChange('benefitDescription', e.target.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default JobPostBenefitFilterPanel;