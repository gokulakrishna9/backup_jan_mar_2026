import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllMarketTrendLocation } from '../../../store/slices/marketTrendLocationSlice';

const MarketTrendLocationFilterPanel = () => {
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
    dispatch(fetchAllMarketTrendLocation({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllMarketTrendLocation({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter MarketTrendLocation</h3>
      <div className="field p-mb-3">
        <label>Location Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.locationId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('locationId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.locationId} onValueChange={(e) => handleFilterChange('locationId', e.value)} />
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
        <label>Country</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.country || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('country', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.country || ''} onChange={(e) => handleFilterChange('country', e.target.value)} />
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
        <label>City</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.city || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('city', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.city || ''} onChange={(e) => handleFilterChange('city', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Job Market Health</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.jobMarketHealth || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('jobMarketHealth', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.jobMarketHealth || ''} onChange={(e) => handleFilterChange('jobMarketHealth', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Unemployment Rate</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.unemploymentRate || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('unemploymentRate', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.unemploymentRate} onValueChange={(e) => handleFilterChange('unemploymentRate', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Average Salary</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.averageSalary || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('averageSalary', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.averageSalary || ''} onChange={(e) => handleFilterChange('averageSalary', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Cost Of Living Index</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.costOfLivingIndex || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('costOfLivingIndex', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.costOfLivingIndex} onValueChange={(e) => handleFilterChange('costOfLivingIndex', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Top Industries</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.topIndustries || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('topIndustries', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.topIndustries || ''} onChange={(e) => handleFilterChange('topIndustries', e.target.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default MarketTrendLocationFilterPanel;