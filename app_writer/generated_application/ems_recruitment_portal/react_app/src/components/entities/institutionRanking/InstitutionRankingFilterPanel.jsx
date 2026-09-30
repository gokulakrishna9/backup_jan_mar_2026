import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllInstitutionRanking } from '../../../store/slices/institutionRankingSlice';

const InstitutionRankingFilterPanel = () => {
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
    dispatch(fetchAllInstitutionRanking({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllInstitutionRanking({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter InstitutionRanking</h3>
      <div className="field p-mb-3">
        <label>Ranking Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.rankingId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('rankingId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.rankingId} onValueChange={(e) => handleFilterChange('rankingId', e.value)} />
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
        <label>Ranking Organization</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.rankingOrganization || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('rankingOrganization', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.rankingOrganization || ''} onChange={(e) => handleFilterChange('rankingOrganization', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Ranking Year</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.rankingYear || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('rankingYear', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.rankingYear} onValueChange={(e) => handleFilterChange('rankingYear', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Overall Rank</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.overallRank || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('overallRank', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.overallRank} onValueChange={(e) => handleFilterChange('overallRank', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Country Rank</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.countryRank || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('countryRank', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.countryRank} onValueChange={(e) => handleFilterChange('countryRank', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Category</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.category || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('category', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.category || ''} onChange={(e) => handleFilterChange('category', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Category Rank</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.categoryRank || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('categoryRank', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.categoryRank} onValueChange={(e) => handleFilterChange('categoryRank', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Score</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.score || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('score', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.score} onValueChange={(e) => handleFilterChange('score', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default InstitutionRankingFilterPanel;