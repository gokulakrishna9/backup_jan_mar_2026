"""Jinja2 template for grouped parent-child form with TabView."""

GROUPED_FORM = """import React, { useState } from 'react';
import { TabView, TabPanel } from 'primereact/tabview';
{% for tab in groupTabs %}import {{ tab.entityName | pascalCase }}Form from '../{{ tab.entityName | camelCase }}/{{ tab.entityName | pascalCase }}Form';
import {{ tab.entityName | pascalCase }}DataTable from '../{{ tab.entityName | camelCase }}/{{ tab.entityName | pascalCase }}DataTable';
{% endfor %}

const {{ entityNamePascal }}GroupedForm = () => {
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
    setSelectedParentId(rowData.{{ pkField }});
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
{% for tab in groupTabs %}      <TabPanel header="{{ tab.tabLabel }}"{% if not loop.first %} disabled={!selectedParentId}{% endif %}>
{% if loop.first %}        <{{ tab.entityName | pascalCase }}Form data={selectedRecord} mode={formMode} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <{{ tab.entityName | pascalCase }}DataTable onRowSelect={handleParentRowSelect} />
{% else %}        <{{ tab.entityName | pascalCase }}Form data={selectedRecord} mode={formMode} parentId={selectedParentId} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
        <{{ tab.entityName | pascalCase }}DataTable onRowSelect={handleRowSelect} />
{% endif %}      </TabPanel>
{% endfor %}    </TabView>
  );
};

export default {{ entityNamePascal }}GroupedForm;
"""
