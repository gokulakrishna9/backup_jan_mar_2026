import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllMarketTrendSkillDemand } from '../../../store/slices/marketTrendSkillDemandSlice';

const MarketTrendSkillDemandFilterPanel = () => {
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
    dispatch(fetchAllMarketTrendSkillDemand({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllMarketTrendSkillDemand({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter MarketTrendSkillDemand</h3>
      <div className="field p-mb-3">
        <label>Demand Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.demandId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('demandId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.demandId} onValueChange={(e) => handleFilterChange('demandId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Trend Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.trendId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('trendId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.trendId} onValueChange={(e) => handleFilterChange('trendId', e.value)} />
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
        <label>Demand Level</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.demandLevel || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('demandLevel', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.demandLevel || ''} onChange={(e) => handleFilterChange('demandLevel', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Growth Rate</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.growthRate || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('growthRate', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.growthRate} onValueChange={(e) => handleFilterChange('growthRate', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Average Salary Range</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.averageSalaryRange || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('averageSalaryRange', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.averageSalaryRange || ''} onChange={(e) => handleFilterChange('averageSalaryRange', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Job Openings Count</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.jobOpeningsCount || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('jobOpeningsCount', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.jobOpeningsCount} onValueChange={(e) => handleFilterChange('jobOpeningsCount', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Region</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.region || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('region', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.region || ''} onChange={(e) => handleFilterChange('region', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Industry</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.industry || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('industry', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.industry || ''} onChange={(e) => handleFilterChange('industry', e.target.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default MarketTrendSkillDemandFilterPanel;