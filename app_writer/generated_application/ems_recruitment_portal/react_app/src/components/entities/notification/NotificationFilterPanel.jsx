import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllNotification } from '../../../store/slices/notificationSlice';

const NotificationFilterPanel = () => {
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
    dispatch(fetchAllNotification({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllNotification({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter Notification</h3>
      <div className="field p-mb-3">
        <label>Notification Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.notificationId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('notificationId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.notificationId} onValueChange={(e) => handleFilterChange('notificationId', e.value)} />
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
        <label>Notification Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.notificationType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('notificationType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.notificationType || ''} onChange={(e) => handleFilterChange('notificationType', e.target.value)} />
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
        <label>Message</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.message || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('message', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.message || ''} onChange={(e) => handleFilterChange('message', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Related Entity Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.relatedEntityType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('relatedEntityType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.relatedEntityType || ''} onChange={(e) => handleFilterChange('relatedEntityType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Related Entity Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.relatedEntityId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('relatedEntityId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.relatedEntityId} onValueChange={(e) => handleFilterChange('relatedEntityId', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Action Url</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.actionUrl || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('actionUrl', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.actionUrl || ''} onChange={(e) => handleFilterChange('actionUrl', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Is Read</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.isRead || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('isRead', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Checkbox checked={!!filters.isRead} onChange={(e) => handleFilterChange('isRead', e.checked)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Read At</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.readAt || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('readAt', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.readAt} onChange={(e) => handleFilterChange('readAt', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Priority</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.priority || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('priority', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.priority || ''} onChange={(e) => handleFilterChange('priority', e.target.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default NotificationFilterPanel;