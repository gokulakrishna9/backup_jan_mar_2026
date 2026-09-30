import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllUserRecommendation } from '../../../store/slices/userRecommendationSlice';

const UserRecommendationFilterPanel = () => {
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
    dispatch(fetchAllUserRecommendation({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllUserRecommendation({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter UserRecommendation</h3>
      <div className="field p-mb-3">
        <label>Recommendation Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.recommendationId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('recommendationId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.recommendationId} onValueChange={(e) => handleFilterChange('recommendationId', e.value)} />
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
        <label>Recommended By User Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.recommendedByUserId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('recommendedByUserId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.recommendedByUserId} onValueChange={(e) => handleFilterChange('recommendedByUserId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Recommendation Text</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.recommendationText || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('recommendationText', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.recommendationText || ''} onChange={(e) => handleFilterChange('recommendationText', e.target.value)} />
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
      <div className="field p-mb-3">
        <label>Position At Time</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.positionAtTime || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('positionAtTime', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.positionAtTime || ''} onChange={(e) => handleFilterChange('positionAtTime', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Visible</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isVisible || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isVisible', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isVisible} onChange={(e) => handleFilterChange('isVisible', e.checked)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default UserRecommendationFilterPanel;