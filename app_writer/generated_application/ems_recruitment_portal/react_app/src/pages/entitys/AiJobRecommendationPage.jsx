import React, { useState } from 'react';
import AiJobRecommendationForm from '../../components/entities/aiJobRecommendation/AiJobRecommendationForm';
import AiJobRecommendationDataTable from '../../components/entities/aiJobRecommendation/AiJobRecommendationDataTable';


const AiJobRecommendationPage = () => {
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [formMode, setFormMode] = useState('view');
  const [showForm, setShowForm] = useState(false);

  const handleRowSelect = (rowData, mode) => {
    setSelectedRecord(rowData);
    setFormMode(mode);
    setShowForm(true);
  };

  const handleNew = () => {
    setSelectedRecord(null);
    setFormMode('create');
    setShowForm(true);
  };

  const handleSave = () => {
    setSelectedRecord(null);
    setFormMode('view');
    setShowForm(false);
  };

  const handleCancel = () => {
    setFormMode('view');
    setShowForm(false);
  };

  return (
    <div>
      <h2 style={ { margin: '0 0 1rem 1rem' } }>Ai Job Recommendation</h2>
      <div
        style={ {
          display: 'grid',
          gridTemplateRows: 'auto 1fr',
          gridTemplateColumns: '1fr',
          gridTemplateAreas: `'form' 'table'`,
          gap: '1rem',
          padding: '0 1rem 1rem 1rem',
        } }
      >
      <div style={ { gridArea: 'form' } }>
        <AiJobRecommendationForm data={selectedRecord} mode={formMode} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
      </div>
      <div style={ { gridArea: 'table' } }>
        <AiJobRecommendationDataTable onRowSelect={handleRowSelect} />
      </div>
      </div>
    </div>
  );
};

export default AiJobRecommendationPage;