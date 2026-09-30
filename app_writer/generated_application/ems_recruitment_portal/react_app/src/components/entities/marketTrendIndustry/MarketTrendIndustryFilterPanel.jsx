import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllMarketTrendIndustry } from '../../../store/slices/marketTrendIndustrySlice';

const MarketTrendIndustryFilterPanel = () => {
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
    dispatch(fetchAllMarketTrendIndustry({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllMarketTrendIndustry({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter MarketTrendIndustry</h3>
      <div className="field p-mb-3">
        <label>Industry Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.industryId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('industryId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.industryId} onValueChange={(e) => handleFilterChange('industryId', e.value)} />
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
        <label>Industry Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.industryName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('industryName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.industryName || ''} onChange={(e) => handleFilterChange('industryName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Description</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.description || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('description', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.description || ''} onChange={(e) => handleFilterChange('description', e.target.value)} />
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
        <label>Market Size</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.marketSize || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('marketSize', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.marketSize || ''} onChange={(e) => handleFilterChange('marketSize', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Emerging Technologies</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.emergingTechnologies || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('emergingTechnologies', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.emergingTechnologies || ''} onChange={(e) => handleFilterChange('emergingTechnologies', e.target.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default MarketTrendIndustryFilterPanel;