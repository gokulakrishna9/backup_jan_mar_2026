import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllCourseCommunityLink } from '../../../store/slices/courseCommunityLinkSlice';

const CourseCommunityLinkFilterPanel = () => {
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
    dispatch(fetchAllCourseCommunityLink({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllCourseCommunityLink({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter CourseCommunityLink</h3>
      <div className="field p-mb-3">
        <label>Link Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.linkId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('linkId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.linkId} onValueChange={(e) => handleFilterChange('linkId', e.value)} />
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
        <label>Community Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.communityId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('communityId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.communityId} onValueChange={(e) => handleFilterChange('communityId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Link Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.linkType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('linkType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.linkType || ''} onChange={(e) => handleFilterChange('linkType', e.target.value)} />
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

export default CourseCommunityLinkFilterPanel;