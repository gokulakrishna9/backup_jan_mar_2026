import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAllSubscriptionPaymentHistory } from '../../../store/slices/subscriptionPaymentHistorySlice';

const SubscriptionPaymentHistoryFilterPanel = () => {
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
    dispatch(fetchAllSubscriptionPaymentHistory({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAllSubscriptionPaymentHistory({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter SubscriptionPaymentHistory</h3>
      <div className="field p-mb-3">
        <label>Payment Id</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.paymentId || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('paymentId', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.paymentId} onValueChange={(e) => handleFilterChange('paymentId', e.value)} />
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
        <label>Amount</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.amount || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('amount', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputNumber value={filters.amount} onValueChange={(e) => handleFilterChange('amount', e.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Subscription Type</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.subscriptionType || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('subscriptionType', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.subscriptionType || ''} onChange={(e) => handleFilterChange('subscriptionType', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Transaction Details</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.transactionDetails || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('transactionDetails', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.transactionDetails || ''} onChange={(e) => handleFilterChange('transactionDetails', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Transaction Reference</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.transactionReference || 'equals'}
            options={ ["equals", "contains", "startsWith", "endsWith", "in"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('transactionReference', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <InputText value={filters.transactionReference || ''} onChange={(e) => handleFilterChange('transactionReference', e.target.value)} />
        </div>
      </div>
      <div className="field p-mb-3">
        <label>Payment On</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.paymentOn || 'equals'}
            options={ ["equals", "greaterThan", "lessThan", "between"] .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('paymentOn', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
          <Calendar value={filters.paymentOn} onChange={(e) => handleFilterChange('paymentOn', e.value)} />
        </div>
      </div>
      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default SubscriptionPaymentHistoryFilterPanel;