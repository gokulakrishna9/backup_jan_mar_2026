import React, { useState } from 'react';
import { TabView, TabPanel } from 'primereact/tabview';
import TrainingExamForm from '../trainingExam/TrainingExamForm';
import TrainingExamDataTable from '../trainingExam/TrainingExamDataTable';
import ExamQuestionForm from '../examQuestion/ExamQuestionForm';
import ExamQuestionDataTable from '../examQuestion/ExamQuestionDataTable';
import ExamAnswerForm from '../examAnswer/ExamAnswerForm';
import ExamAnswerDataTable from '../examAnswer/ExamAnswerDataTable';


const TrainingExamGroupedForm = () => {
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
    setSelectedParentId(rowData.trainingExamId);
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
      <TabPanel header="Exam Details">
        <TrainingExamForm data={selectedRecord} mode={formMode} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <TrainingExamDataTable onRowSelect={handleParentRowSelect} />
      </TabPanel>
      <TabPanel header="Questions" disabled={!selectedParentId}>
        <ExamQuestionForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <ExamQuestionDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
      <TabPanel header="Answers" disabled={!selectedParentId}>
        <ExamAnswerForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <ExamAnswerDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
    </TabView>
  );
};

export default TrainingExamGroupedForm;