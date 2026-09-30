import React, { useState } from 'react';
import { TabView, TabPanel } from 'primereact/tabview';
import CourseQuestionForm from '../courseQuestion/CourseQuestionForm';
import CourseQuestionDataTable from '../courseQuestion/CourseQuestionDataTable';
import CourseAnswerForm from '../courseAnswer/CourseAnswerForm';
import CourseAnswerDataTable from '../courseAnswer/CourseAnswerDataTable';


const CourseQuestionGroupedForm = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [selectedParentId, setSelectedParentId] = useState(null);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [formMode, setFormMode] = useState('view');
  const [showForm, setShowForm] = useState(false);

  const handleRowSelect = (rowData, mode) => {
    setSelectedRecord(rowData);
    setFormMode(mode || 'view');
    setShowForm(true);
  };

  const handleParentRowSelect = (rowData, mode) => {
    setSelectedParentId(rowData.courseQuestionId);
    handleRowSelect(rowData, mode);
  };

  const handleSave = () => {
    setFormMode('view');
    setShowForm(false);
  };

  const handleCancel = () => {
    setFormMode('view');
    setShowForm(false);
  };

  const handleNew = () => {
    setSelectedRecord(null);
    setFormMode('create');
    setShowForm(true);
  };

  return (
    <TabView activeIndex={activeIndex} onTabChange={(e) => { setActiveIndex(e.index); setSelectedRecord(null); setFormMode('view'); setShowForm(false); }}>
      <TabPanel header="Questions">
        <CourseQuestionForm data={selectedRecord} mode={formMode} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <CourseQuestionDataTable onRowSelect={handleParentRowSelect} />
      </TabPanel>
      <TabPanel header="Answers" disabled={!selectedParentId}>
        <CourseAnswerForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <CourseAnswerDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
    </TabView>
  );
};

export default CourseQuestionGroupedForm;