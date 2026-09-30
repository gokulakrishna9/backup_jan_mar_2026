import React, { useState } from 'react';
import { TabView, TabPanel } from 'primereact/tabview';
import UserEducationForm from '../userEducation/UserEducationForm';
import UserEducationDataTable from '../userEducation/UserEducationDataTable';
import UserWorkExperienceForm from '../userWorkExperience/UserWorkExperienceForm';
import UserWorkExperienceDataTable from '../userWorkExperience/UserWorkExperienceDataTable';
import UserSkillForm from '../userSkill/UserSkillForm';
import UserSkillDataTable from '../userSkill/UserSkillDataTable';


const UserEducationGroupedForm = () => {
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
    setSelectedParentId(rowData.userEducationId);
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
      <TabPanel header="Education">
        <UserEducationForm data={selectedRecord} mode={formMode} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <UserEducationDataTable onRowSelect={handleParentRowSelect} />
      </TabPanel>
      <TabPanel header="Work Experience" disabled={!selectedParentId}>
        <UserWorkExperienceForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <UserWorkExperienceDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
      <TabPanel header="Skills" disabled={!selectedParentId}>
        <UserSkillForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <UserSkillDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
    </TabView>
  );
};

export default UserEducationGroupedForm;