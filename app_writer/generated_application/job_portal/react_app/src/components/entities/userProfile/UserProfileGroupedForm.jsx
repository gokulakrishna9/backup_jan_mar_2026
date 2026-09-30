import React, { useState } from 'react';
import { TabView, TabPanel } from 'primereact/tabview';
import UserProfileForm from '../userProfile/UserProfileForm';
import UserProfileDataTable from '../userProfile/UserProfileDataTable';
import StudentProfileForm from '../studentProfile/StudentProfileForm';
import StudentProfileDataTable from '../studentProfile/StudentProfileDataTable';
import EmployerProfileForm from '../employerProfile/EmployerProfileForm';
import EmployerProfileDataTable from '../employerProfile/EmployerProfileDataTable';
import TrainerProfileForm from '../trainerProfile/TrainerProfileForm';
import TrainerProfileDataTable from '../trainerProfile/TrainerProfileDataTable';


const UserProfileGroupedForm = () => {
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
    setSelectedParentId(rowData.userProfileId);
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
      <TabPanel header="Basic Info">
        <UserProfileForm data={selectedRecord} mode={formMode} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <UserProfileDataTable onRowSelect={handleParentRowSelect} />
      </TabPanel>
      <TabPanel header="Student" disabled={!selectedParentId}>
        <StudentProfileForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <StudentProfileDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
      <TabPanel header="Employer" disabled={!selectedParentId}>
        <EmployerProfileForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <EmployerProfileDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
      <TabPanel header="Trainer" disabled={!selectedParentId}>
        <TrainerProfileForm data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <TrainerProfileDataTable onRowSelect={handleRowSelect} />
      </TabPanel>
    </TabView>
  );
};

export default UserProfileGroupedForm;