import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllMarketTrendInstitutionLink } from '../../../store/slices/marketTrendInstitutionLinkSlice';

const MarketTrendInstitutionLinkFilterPanel = () => {
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
    dispatch(fetchAllMarketTrendInstitutionLink({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllMarketTrendInstitutionLink({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter MarketTrendInstitutionLink</h3>
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
        <label>Institution Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.institutionId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('institutionId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.institutionId} onValueChange={(e) => handleFilterChange('institutionId', e.value)} />
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
        <label>Specialization Areas</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.specializationAreas || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('specializationAreas', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.specializationAreas || ''} onChange={(e) => handleFilterChange('specializationAreas', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Partnership Opportunities</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.partnershipOpportunities || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('partnershipOpportunities', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.partnershipOpportunities || ''} onChange={(e) => handleFilterChange('partnershipOpportunities', e.target.value)} />
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

export default MarketTrendInstitutionLinkFilterPanel;