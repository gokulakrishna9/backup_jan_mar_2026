"""Jinja2 template for per-entity filter panel components."""

FILTER_PANEL = """import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { fetchAll{{ entityNamePascal }} } from '../../../store/slices/{{ entityNameCamel }}Slice';

const {{ entityNamePascal }}FilterPanel = () => {
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
    dispatch(fetchAll{{ entityNamePascal }}({ filter: filterParams }));
  };

  const handleClear = () => {
    setFilters({});
    setOperators({});
    dispatch(fetchAll{{ entityNamePascal }}({}));
  };

  return (
    <div className="p-fluid">
      <h3>Filter {{ entityNamePascal }}</h3>
{% for field in filterFields %}      <div className="field p-mb-3">
        <label>{{ field.fieldLabel }}</label>
        <div className="p-d-flex p-ai-center">
          <Dropdown
            value={operators.{{ field.fieldName }} || '{{ field.operators[0] if field.operators else "EQUALS" }}'}
            options={ {{ field.operators | tojson }} .map((op) => ({ label: op, value: op }))}
            onChange={(e) => handleOperatorChange('{{ field.fieldName }}', e.value)}
            className="p-mr-2"
            style={ { width: '10rem' } }
          />
{% if field.componentType == 'InputText' %}          <InputText value={filters.{{ field.fieldName }} || ''} onChange={(e) => handleFilterChange('{{ field.fieldName }}', e.target.value)} />
{% elif field.componentType == 'InputNumber' %}          <InputNumber value={filters.{{ field.fieldName }}} onValueChange={(e) => handleFilterChange('{{ field.fieldName }}', e.value)} />
{% elif field.componentType == 'Calendar' %}          <Calendar value={filters.{{ field.fieldName }}} onChange={(e) => handleFilterChange('{{ field.fieldName }}', e.value)} />
{% elif field.componentType == 'Checkbox' %}          <Checkbox checked={!!filters.{{ field.fieldName }}} onChange={(e) => handleFilterChange('{{ field.fieldName }}', e.checked)} />
{% else %}          <InputText value={filters.{{ field.fieldName }} || ''} onChange={(e) => handleFilterChange('{{ field.fieldName }}', e.target.value)} />
{% endif %}        </div>
      </div>
{% endfor %}      <div className="p-d-flex p-jc-end p-mt-3">
        <Button label="Apply" icon="pi pi-filter" className="p-mr-2" onClick={handleApply} />
        <Button label="Clear" icon="pi pi-times" className="p-button-secondary" onClick={handleClear} />
      </div>
    </div>
  );
};

export default {{ entityNamePascal }}FilterPanel;
"""
