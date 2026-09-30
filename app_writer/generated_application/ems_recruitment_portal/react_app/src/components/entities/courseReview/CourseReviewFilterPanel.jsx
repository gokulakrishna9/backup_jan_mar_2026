import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllCourseReview } from '../../../store/slices/courseReviewSlice';

const CourseReviewFilterPanel = () => {
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
    dispatch(fetchAllCourseReview({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllCourseReview({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter CourseReview</h3>
      <div className="field p-mb-3">
        <label>Review Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.reviewId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('reviewId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.reviewId} onValueChange={(e) => handleFilterChange('reviewId', e.value)} />
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
        <label>Rating</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.rating || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('rating', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.rating} onValueChange={(e) => handleFilterChange('rating', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Review Title</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.reviewTitle || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('reviewTitle', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.reviewTitle || ''} onChange={(e) => handleFilterChange('reviewTitle', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Review Text</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.reviewText || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('reviewText', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.reviewText || ''} onChange={(e) => handleFilterChange('reviewText', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Helpful Count</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.helpfulCount || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('helpfulCount', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.helpfulCount} onValueChange={(e) => handleFilterChange('helpfulCount', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Verified Purchase</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isVerifiedPurchase || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isVerifiedPurchase', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isVerifiedPurchase} onChange={(e) => handleFilterChange('isVerifiedPurchase', e.checked)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default CourseReviewFilterPanel;