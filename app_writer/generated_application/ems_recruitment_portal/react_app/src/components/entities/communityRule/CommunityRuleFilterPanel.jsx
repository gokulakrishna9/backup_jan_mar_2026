import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllCommunityRule } from '../../../store/slices/communityRuleSlice';

const CommunityRuleFilterPanel = () => {
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
    dispatch(fetchAllCommunityRule({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllCommunityRule({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter CommunityRule</h3>
      <div className="field p-mb-3">
        <label>Rule Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.ruleId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('ruleId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.ruleId} onValueChange={(e) => handleFilterChange('ruleId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Community Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.communityId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('communityId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.communityId} onValueChange={(e) => handleFilterChange('communityId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Rule Title</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.ruleTitle || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('ruleTitle', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.ruleTitle || ''} onChange={(e) => handleFilterChange('ruleTitle', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Rule Description</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.ruleDescription || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('ruleDescription', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.ruleDescription || ''} onChange={(e) => handleFilterChange('ruleDescription', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Order Sequence</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.orderSequence || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('orderSequence', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.orderSequence} onValueChange={(e) => handleFilterChange('orderSequence', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default CommunityRuleFilterPanel;