import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllCourse } from '../../../store/slices/courseSlice';

const CourseFilterPanel = () => {
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
    dispatch(fetchAllCourse({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllCourse({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter Course</h3>
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
        <label>Course Name</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.courseName || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('courseName', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.courseName || ''} onChange={(e) => handleFilterChange('courseName', e.target.value)} />
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
        <label>Outcomes</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.outcomes || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('outcomes', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.outcomes || ''} onChange={(e) => handleFilterChange('outcomes', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Course Type Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.courseTypeId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('courseTypeId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.courseTypeId} onValueChange={(e) => handleFilterChange('courseTypeId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Published</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isPublished || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isPublished', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isPublished} onChange={(e) => handleFilterChange('isPublished', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Price</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.price || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('price', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.price} onValueChange={(e) => handleFilterChange('price', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Duration Weeks</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.durationWeeks || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('durationWeeks', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.durationWeeks} onValueChange={(e) => handleFilterChange('durationWeeks', e.value)} />
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

export default CourseFilterPanel;