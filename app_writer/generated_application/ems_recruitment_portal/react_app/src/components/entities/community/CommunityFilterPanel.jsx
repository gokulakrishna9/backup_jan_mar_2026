import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllCommunity } from '../../../store/slices/communitySlice';

const CommunityFilterPanel = () => {
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
    dispatch(fetchAllCommunity({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllCommunity({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter Community</h3>
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
        <label>Institute Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.instituteId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('instituteId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.instituteId} onValueChange={(e) => handleFilterChange('instituteId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.name || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('name', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.name || ''} onChange={(e) => handleFilterChange('name', e.target.value)} />
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
        <label>Group Owner User Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.groupOwnerUserId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('groupOwnerUserId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.groupOwnerUserId} onValueChange={(e) => handleFilterChange('groupOwnerUserId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Entity</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isEntity || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isEntity', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isEntity} onChange={(e) => handleFilterChange('isEntity', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Public</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isPublic || 'equals'}
            options={ ["equals"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isPublic', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isPublic} onChange={(e) => handleFilterChange('isPublic', e.checked)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default CommunityFilterPanel;