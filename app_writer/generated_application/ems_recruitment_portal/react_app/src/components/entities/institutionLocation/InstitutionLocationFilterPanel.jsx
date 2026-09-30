import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllInstitutionLocation } from '../../../store/slices/institutionLocationSlice';

const InstitutionLocationFilterPanel = () => {
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
    dispatch(fetchAllInstitutionLocation({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllInstitutionLocation({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter InstitutionLocation</h3>
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
        <label>Location Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.locationType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('locationType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.locationType || ''} onChange={(e) => handleFilterChange('locationType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Address Line1</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.addressLine1 || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('addressLine1', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.addressLine1 || ''} onChange={(e) => handleFilterChange('addressLine1', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Address Line2</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.addressLine2 || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('addressLine2', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.addressLine2 || ''} onChange={(e) => handleFilterChange('addressLine2', e.target.value)} />
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
        <label>State Province</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.stateProvince || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('stateProvince', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.stateProvince || ''} onChange={(e) => handleFilterChange('stateProvince', e.target.value)} />
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
        <label>Postal Code</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.postalCode || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('postalCode', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.postalCode || ''} onChange={(e) => handleFilterChange('postalCode', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Latitude</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.latitude || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('latitude', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.latitude} onValueChange={(e) => handleFilterChange('latitude', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Longitude</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.longitude || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('longitude', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.longitude} onValueChange={(e) => handleFilterChange('longitude', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Primary</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isPrimary || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isPrimary', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isPrimary} onChange={(e) => handleFilterChange('isPrimary', e.checked)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default InstitutionLocationFilterPanel;