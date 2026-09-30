"""Jinja2 template for per-entity query section components."""

QUERY_SECTION = """import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Button } from 'primereact/button';
import { Accordion, AccordionTab } from 'primereact/accordion';
import apiClient from '../../../services/apiClient';

const {{ entityNamePascal }}QuerySection = ({ onResults }) => {
  const [queryParams, setQueryParams] = useState({});
  const [loading, setLoading] = useState(false);

  const handleParamChange = (queryName, paramName, value) => {
    setQueryParams((prev) => ({
      ...prev,
      [`${queryName}.${paramName}`]: value,
    }));
  };

  const executeQuery = async (queryName, params) => {
    setLoading(true);
    try {
      const queryData = {};
      Object.entries(queryParams).forEach(([key, value]) => {
        if (key.startsWith(`${queryName}.`)) {
          const paramName = key.substring(queryName.length + 1);
          queryData[paramName] = value;
        }
      });
      const response = await apiClient.post(`/api/{{ entityNameCamel }}/query/${queryName}`, queryData);
      if (onResults) onResults(response.data);
    } catch (err) {
      console.error('Query execution failed:', err);
    }
    setLoading(false);
  };

  return (
    <div>
      <h3>Queries for {{ entityNamePascal }}</h3>
      <Accordion>
{% for query in queries %}        <AccordionTab header="{{ query.queryName }}">
          <p>{{ query.description }}</p>
{% for param in query.parameters %}          <div className="field p-mb-2">
            <label>{{ param.name }}{% if param.required %} *{% endif %}</label>
{% if param.componentType == 'InputText' %}            <InputText value={queryParams['{{ query.queryName }}.{{ param.name }}'] || ''} onChange={(e) => handleParamChange('{{ query.queryName }}', '{{ param.name }}', e.target.value)} />
{% elif param.componentType == 'InputNumber' %}            <InputNumber value={queryParams['{{ query.queryName }}.{{ param.name }}']} onValueChange={(e) => handleParamChange('{{ query.queryName }}', '{{ param.name }}', e.value)} />
{% elif param.componentType == 'Calendar' %}            <Calendar value={queryParams['{{ query.queryName }}.{{ param.name }}']} onChange={(e) => handleParamChange('{{ query.queryName }}', '{{ param.name }}', e.value)} />
{% else %}            <InputText value={queryParams['{{ query.queryName }}.{{ param.name }}'] || ''} onChange={(e) => handleParamChange('{{ query.queryName }}', '{{ param.name }}', e.target.value)} />
{% endif %}          </div>
{% endfor %}          <Button label="Execute" icon="pi pi-play" loading={loading} onClick={() => executeQuery('{{ query.queryName }}')} />
        </AccordionTab>
{% endfor %}      </Accordion>
    </div>
  );
};

export default {{ entityNamePascal }}QuerySection;
"""
