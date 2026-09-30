import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllUserCertification } from '../../../store/slices/userCertificationSlice';

const UserCertificationFilterPanel = () => {
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
    dispatch(fetchAllUserCertification({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllUserCertification({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter UserCertification</h3>
      <div className="field p-mb-3">
        <label>Certification Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.certificationId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('certificationId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.certificationId} onValueChange={(e) => handleFilterChange('certificationId', e.value)} />
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
        <label>Certification Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.certificationName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('certificationName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.certificationName || ''} onChange={(e) => handleFilterChange('certificationName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Issuing Organization</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.issuingOrganization || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('issuingOrganization', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.issuingOrganization || ''} onChange={(e) => handleFilterChange('issuingOrganization', e.target.value)} />
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
        <label>Credential Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.credentialId || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('credentialId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.credentialId || ''} onChange={(e) => handleFilterChange('credentialId', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Credential Url</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.credentialUrl || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('credentialUrl', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.credentialUrl || ''} onChange={(e) => handleFilterChange('credentialUrl', e.target.value)} />
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
        <label>Is Verified</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isVerified || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isVerified', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isVerified} onChange={(e) => handleFilterChange('isVerified', e.checked)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default UserCertificationFilterPanel;