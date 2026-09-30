import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllCoursePrerequisite } from '../../../store/slices/coursePrerequisiteSlice';

const CoursePrerequisiteFilterPanel = () => {
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
    dispatch(fetchAllCoursePrerequisite({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllCoursePrerequisite({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter CoursePrerequisite</h3>
      <div className="field p-mb-3">
        <label>Prerequisite Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.prerequisiteId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('prerequisiteId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.prerequisiteId} onValueChange={(e) => handleFilterChange('prerequisiteId', e.value)} />
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
      <div className="field p-mb-3">
        <label>Prerequisite Course Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.prerequisiteCourseId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('prerequisiteCourseId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.prerequisiteCourseId} onValueChange={(e) => handleFilterChange('prerequisiteCourseId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Prerequisite Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.prerequisiteType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('prerequisiteType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.prerequisiteType || ''} onChange={(e) => handleFilterChange('prerequisiteType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Prerequisite Description</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.prerequisiteDescription || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('prerequisiteDescription', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.prerequisiteDescription || ''} onChange={(e) => handleFilterChange('prerequisiteDescription', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Mandatory</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isMandatory || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isMandatory', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isMandatory} onChange={(e) => handleFilterChange('isMandatory', e.checked)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default CoursePrerequisiteFilterPanel;