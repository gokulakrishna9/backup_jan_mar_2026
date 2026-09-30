import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllInstitutionAccreditation } from '../../../store/slices/institutionAccreditationSlice';

const InstitutionAccreditationFilterPanel = () => {
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
    dispatch(fetchAllInstitutionAccreditation({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllInstitutionAccreditation({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter InstitutionAccreditation</h3>
      <div className="field p-mb-3">
        <label>Accreditation Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.accreditationId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('accreditationId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.accreditationId} onValueChange={(e) => handleFilterChange('accreditationId', e.value)} />
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
        <label>Accrediting Body</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.accreditingBody || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('accreditingBody', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.accreditingBody || ''} onChange={(e) => handleFilterChange('accreditingBody', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Accreditation Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.accreditationType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('accreditationType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.accreditationType || ''} onChange={(e) => handleFilterChange('accreditationType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Accreditation Level</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.accreditationLevel || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('accreditationLevel', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.accreditationLevel || ''} onChange={(e) => handleFilterChange('accreditationLevel', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Issue Date</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.issueDate || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('issueDate', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.issueDate} onChange={(e) => handleFilterChange('issueDate', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Expiry Date</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.expiryDate || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('expiryDate', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.expiryDate} onChange={(e) => handleFilterChange('expiryDate', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Certificate Document Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.certificateDocumentId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('certificateDocumentId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.certificateDocumentId} onValueChange={(e) => handleFilterChange('certificateDocumentId', e.value)} />
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

export default InstitutionAccreditationFilterPanel;