import React, { useState } from 'react';
import { TabView, TabPanel } from 'primereact/tabview';
import TrainingProgramForm from '../trainingProgram/TrainingProgramForm';
import TrainingProgramDataTable from '../trainingProgram/TrainingProgramDataTable';
import TrainingModuleForm from '../trainingModule/TrainingModuleForm';
import TrainingModuleDataTable from '../trainingModule/TrainingModuleDataTable';
import CourseDocumentForm from '../courseDocument/CourseDocumentForm';
import CourseDocumentDataTable from '../courseDocument/CourseDocumentDataTable';
import CourseVideoForm from '../courseVideo/CourseVideoForm';
import CourseVideoDataTable from '../courseVideo/CourseVideoDataTable';
import CourseAudioForm from '../courseAudio/CourseAudioForm';
import CourseAudioDataTable from '../courseAudio/CourseAudioDataTable';
import CourseCodeLabForm from '../courseCodeLab/CourseCodeLabForm';
import CourseCodeLabDataTable from '../courseCodeLab/CourseCodeLabDataTable';


const TrainingProgramGroupedForm = () => {
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
    setSelectedParentId(rowData.trainingProgramId);
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
      <TabPanel header="Overview">
        <TrainingProgramForm data={selectedRecord} mode={formMode} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <TrainingProgramDataTable onRowSelect={handleParentRowSelect} />
      </TabPanel>
      <TabPanel header="Modules" disabled={!selectedParentId}>
        <TrainingModuleForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <TrainingModuleDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
      <TabPanel header="Documents" disabled={!selectedParentId}>
        <CourseDocumentForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <CourseDocumentDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
      <TabPanel header="Videos" disabled={!selectedParentId}>
        <CourseVideoForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <CourseVideoDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
      <TabPanel header="Audio" disabled={!selectedParentId}>
        <CourseAudioForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <CourseAudioDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
      <TabPanel header="Code Labs" disabled={!selectedParentId}>
        <CourseCodeLabForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <CourseCodeLabDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
    </TabView>
  );
};

export default TrainingProgramGroupedForm;