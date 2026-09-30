import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';
import { Button } from 'primereact/button';
import { Accordion, AccordionTab } from 'primereact/accordion';
import apiClient from '../../../services/apiClient';

const JobPostQuerySection = ({ onResults }) => {
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
      const response = await apiClient.post(`/api/jobPost/query/${queryName}`, queryData);
      if (onResults) onResults(response.data);
    } catch (err) {
      console.error('Query execution failed:', err);
    }
    setLoading(false);
  };

  return (
    <div>
      <h3>Queries for JobPost</h3>
      <Accordion>
        <AccordionTab header="listJobPost">
          <p>List all JobPost records</p>
          <Button label="Execute" icon="pi pi-play" loading={loading} onClick={() => executeQuery('listJobPost')} />
        </AccordionTab>
      </Accordion>
    </div>
  );
};

export default JobPostQuerySection;