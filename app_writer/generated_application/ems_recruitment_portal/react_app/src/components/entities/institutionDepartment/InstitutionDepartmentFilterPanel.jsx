import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllInstitutionDepartment } from '../../../store/slices/institutionDepartmentSlice';

const InstitutionDepartmentFilterPanel = () => {
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
    dispatch(fetchAllInstitutionDepartment({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllInstitutionDepartment({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter InstitutionDepartment</h3>
      <div className="field p-mb-3">
        <label>Department Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.departmentId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('departmentId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.departmentId} onValueChange={(e) => handleFilterChange('departmentId', e.value)} />
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
        <label>Department Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.departmentName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('departmentName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.departmentName || ''} onChange={(e) => handleFilterChange('departmentName', e.target.value)} />
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
        <label>Head Of Department User Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.headOfDepartmentUserId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('headOfDepartmentUserId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.headOfDepartmentUserId} onValueChange={(e) => handleFilterChange('headOfDepartmentUserId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Contact Email</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.contactEmail || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('contactEmail', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.contactEmail || ''} onChange={(e) => handleFilterChange('contactEmail', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Contact Phone</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.contactPhone || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('contactPhone', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.contactPhone || ''} onChange={(e) => handleFilterChange('contactPhone', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Active</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isActive || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isActive', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isActive} onChange={(e) => handleFilterChange('isActive', e.checked)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default InstitutionDepartmentFilterPanel;