import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllMarketTrendJobPostLink } from '../../../store/slices/marketTrendJobPostLinkSlice';

const MarketTrendJobPostLinkFilterPanel = () => {
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
    dispatch(fetchAllMarketTrendJobPostLink({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllMarketTrendJobPostLink({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter MarketTrendJobPostLink</h3>
      <div className="field p-mb-3">
        <label>Link Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.linkId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('linkId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.linkId} onValueChange={(e) => handleFilterChange('linkId', e.value)} />
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
        <label>Relevance Score</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.relevanceScore || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('relevanceScore', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.relevanceScore} onValueChange={(e) => handleFilterChange('relevanceScore', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Growth Potential</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.growthPotential || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('growthPotential', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.growthPotential || ''} onChange={(e) => handleFilterChange('growthPotential', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Salary Trend</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.salaryTrend || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('salaryTrend', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.salaryTrend || ''} onChange={(e) => handleFilterChange('salaryTrend', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Ai Generated</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.aiGenerated || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('aiGenerated', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.aiGenerated} onChange={(e) => handleFilterChange('aiGenerated', e.checked)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default MarketTrendJobPostLinkFilterPanel;