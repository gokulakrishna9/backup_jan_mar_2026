import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllCourseProperty } from '../../../store/slices/coursePropertySlice';

const CoursePropertyFilterPanel = () => {
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
    dispatch(fetchAllCourseProperty({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllCourseProperty({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter CourseProperty</h3>
      <div className="field p-mb-3">
        <label>Property Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.propertyId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('propertyId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.propertyId} onValueChange={(e) => handleFilterChange('propertyId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Property Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.propertyName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('propertyName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.propertyName || ''} onChange={(e) => handleFilterChange('propertyName', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Property Value</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.propertyValue || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('propertyValue', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.propertyValue || ''} onChange={(e) => handleFilterChange('propertyValue', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Property Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.propertyType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('propertyType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.propertyType || ''} onChange={(e) => handleFilterChange('propertyType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Property Description</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.propertyDescription || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('propertyDescription', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.propertyDescription || ''} onChange={(e) => handleFilterChange('propertyDescription', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Group Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.groupId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('groupId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.groupId} onValueChange={(e) => handleFilterChange('groupId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Course Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.courseId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('courseId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.courseId} onValueChange={(e) => handleFilterChange('courseId', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default CoursePropertyFilterPanel;