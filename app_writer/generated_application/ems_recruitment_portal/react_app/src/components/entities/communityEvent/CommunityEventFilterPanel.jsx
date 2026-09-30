import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllCommunityEvent } from '../../../store/slices/communityEventSlice';

const CommunityEventFilterPanel = () => {
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
    dispatch(fetchAllCommunityEvent({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllCommunityEvent({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter CommunityEvent</h3>
      <div className="field p-mb-3">
        <label>Event Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.eventId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('eventId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.eventId} onValueChange={(e) => handleFilterChange('eventId', e.value)} />
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
        <label>Event Title</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.eventTitle || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('eventTitle', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.eventTitle || ''} onChange={(e) => handleFilterChange('eventTitle', e.target.value)} />
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
        <label>Event Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.eventType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('eventType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.eventType || ''} onChange={(e) => handleFilterChange('eventType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Start Datetime</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.startDatetime || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('startDatetime', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.startDatetime} onChange={(e) => handleFilterChange('startDatetime', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>End Datetime</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.endDatetime || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('endDatetime', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.endDatetime} onChange={(e) => handleFilterChange('endDatetime', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Location</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.location || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('location', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.location || ''} onChange={(e) => handleFilterChange('location', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Meeting Link</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.meetingLink || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('meetingLink', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.meetingLink || ''} onChange={(e) => handleFilterChange('meetingLink', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Max Attendees</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.maxAttendees || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('maxAttendees', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.maxAttendees} onValueChange={(e) => handleFilterChange('maxAttendees', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Organizer User Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.organizerUserId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('organizerUserId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.organizerUserId} onValueChange={(e) => handleFilterChange('organizerUserId', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default CommunityEventFilterPanel;