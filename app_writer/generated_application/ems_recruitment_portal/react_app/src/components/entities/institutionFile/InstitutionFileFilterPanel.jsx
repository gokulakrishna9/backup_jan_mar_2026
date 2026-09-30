import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllInstitutionFile } from '../../../store/slices/institutionFileSlice';

const InstitutionFileFilterPanel = () => {
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
    dispatch(fetchAllInstitutionFile({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllInstitutionFile({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter InstitutionFile</h3>
      <div className="field p-mb-3">
        <label>File Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.fileId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('fileId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.fileId} onValueChange={(e) => handleFilterChange('fileId', e.value)} />
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
        <label>File Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.fileName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('fileName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.fileName || ''} onChange={(e) => handleFilterChange('fileName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Original File Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.originalFileName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('originalFileName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.originalFileName || ''} onChange={(e) => handleFilterChange('originalFileName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>File Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.fileType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('fileType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.fileType || ''} onChange={(e) => handleFilterChange('fileType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>File Extension</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.fileExtension || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('fileExtension', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.fileExtension || ''} onChange={(e) => handleFilterChange('fileExtension', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>File Location</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.fileLocation || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('fileLocation', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.fileLocation || ''} onChange={(e) => handleFilterChange('fileLocation', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>File Size Bytes</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.fileSizeBytes || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('fileSizeBytes', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.fileSizeBytes} onValueChange={(e) => handleFilterChange('fileSizeBytes', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Mime Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.mimeType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('mimeType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.mimeType || ''} onChange={(e) => handleFilterChange('mimeType', e.target.value)} />
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
        <label>Comment</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.comment || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('comment', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.comment || ''} onChange={(e) => handleFilterChange('comment', e.target.value)} />
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
      <div className="field p-mb-3">
        <label>Download Count</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.downloadCount || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('downloadCount', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.downloadCount} onValueChange={(e) => handleFilterChange('downloadCount', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Thumbnail Location</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.thumbnailLocation || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('thumbnailLocation', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.thumbnailLocation || ''} onChange={(e) => handleFilterChange('thumbnailLocation', e.target.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default InstitutionFileFilterPanel;