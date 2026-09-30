import React, { useState } from 'react';
import CourseQuestionGroupedForm from '../../components/entities/courseQuestion/CourseQuestionGroupedForm';


const CourseQuestionPage = () => {
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
      <h2 style={ { margin: '0 0 1rem 1rem' } }>Course Question</h2>
      <div
        style={ {
          display: 'grid',
          gridTemplateRows: '1fr',
          gridTemplateColumns: '1fr',
          gridTemplateAreas: `'content'`,
          gap: '1rem',
          padding: '0 1rem 1rem 1rem',
        } }
      >
      <div style={ { gridArea: 'content' } }>
        <CourseQuestionGroupedForm />
      </div>
      </div>
    </div>
  );
};

export default CourseQuestionPage;