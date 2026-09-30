import React, { useState } from 'react';
import AiCommunityPostEvaluationForm from '../../components/entities/aiCommunityPostEvaluation/AiCommunityPostEvaluationForm';
import AiCommunityPostEvaluationDataTable from '../../components/entities/aiCommunityPostEvaluation/AiCommunityPostEvaluationDataTable';


const AiCommunityPostEvaluationPage = () => {
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
      <h2 style={ { margin: '0 0 1rem 1rem' } }>Ai Community Post Evaluation</h2>
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
        <AiCommunityPostEvaluationForm data={selectedRecord} mode={formMode} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
      </div>
      <div style={ { gridArea: 'table' } }>
        <AiCommunityPostEvaluationDataTable onRowSelect={handleRowSelect} />
      </div>
      </div>
    </div>
  );
};

export default AiCommunityPostEvaluationPage;