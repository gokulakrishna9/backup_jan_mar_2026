import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllCourseAssignment } from '../../../store/slices/courseAssignmentSlice';

const CourseAssignmentFilterPanel = () => {
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
    dispatch(fetchAllCourseAssignment({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllCourseAssignment({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter CourseAssignment</h3>
      <div className="field p-mb-3">
        <label>Assignment Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.assignmentId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('assignmentId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.assignmentId} onValueChange={(e) => handleFilterChange('assignmentId', e.value)} />
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
        <label>Module Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.moduleId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('moduleId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.moduleId} onValueChange={(e) => handleFilterChange('moduleId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Title</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.title || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('title', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.title || ''} onChange={(e) => handleFilterChange('title', e.target.value)} />
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
        <label>Assignment Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.assignmentType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('assignmentType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.assignmentType || ''} onChange={(e) => handleFilterChange('assignmentType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Max Score</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.maxScore || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('maxScore', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.maxScore} onValueChange={(e) => handleFilterChange('maxScore', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Passing Score</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.passingScore || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('passingScore', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.passingScore} onValueChange={(e) => handleFilterChange('passingScore', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Due Date</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.dueDate || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('dueDate', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.dueDate} onChange={(e) => handleFilterChange('dueDate', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Duration Minutes</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.durationMinutes || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('durationMinutes', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.durationMinutes} onValueChange={(e) => handleFilterChange('durationMinutes', e.value)} />
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

export default CourseAssignmentFilterPanel;