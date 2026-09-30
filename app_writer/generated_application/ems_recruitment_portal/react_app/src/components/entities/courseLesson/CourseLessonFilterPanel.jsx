import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllCourseLesson } from '../../../store/slices/courseLessonSlice';

const CourseLessonFilterPanel = () => {
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
    dispatch(fetchAllCourseLesson({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllCourseLesson({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter CourseLesson</h3>
      <div className="field p-mb-3">
        <label>Lesson Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.lessonId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('lessonId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.lessonId} onValueChange={(e) => handleFilterChange('lessonId', e.value)} />
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
        <label>Lesson Title</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.lessonTitle || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('lessonTitle', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.lessonTitle || ''} onChange={(e) => handleFilterChange('lessonTitle', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Lesson Number</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.lessonNumber || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('lessonNumber', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.lessonNumber} onValueChange={(e) => handleFilterChange('lessonNumber', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Content Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.contentType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('contentType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.contentType || ''} onChange={(e) => handleFilterChange('contentType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Content Url</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.contentUrl || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('contentUrl', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.contentUrl || ''} onChange={(e) => handleFilterChange('contentUrl', e.target.value)} />
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
        <label>Is Preview Available</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isPreviewAvailable || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isPreviewAvailable', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isPreviewAvailable} onChange={(e) => handleFilterChange('isPreviewAvailable', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Order Sequence</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.orderSequence || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('orderSequence', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.orderSequence} onValueChange={(e) => handleFilterChange('orderSequence', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default CourseLessonFilterPanel;