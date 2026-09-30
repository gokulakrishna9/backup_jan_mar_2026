"""Jinja2 template for per-entity page components with CSS Grid layout."""

ENTITY_PAGE = """import React, { useState } from 'react';
{% for placement in componentPlacements %}{% if placement.componentType == 'form' %}import {{ entityNamePascal }}Form from '../../components/entities/{{ entityNameCamel }}/{{ entityNamePascal }}Form';
{% elif placement.componentType == 'dataTable' %}import {{ entityNamePascal }}DataTable from '../../components/entities/{{ entityNameCamel }}/{{ entityNamePascal }}DataTable';
{% elif placement.componentType == 'groupedForm' %}import {{ entityNamePascal }}GroupedForm from '../../components/entities/{{ entityNameCamel }}/{{ entityNamePascal }}GroupedForm';
{% elif placement.componentType == 'filterPanel' %}import {{ entityNamePascal }}FilterPanel from '../../components/entities/{{ entityNameCamel }}/{{ entityNamePascal }}FilterPanel';
{% elif placement.componentType == 'querySection' %}import {{ entityNamePascal }}QuerySection from '../../components/entities/{{ entityNameCamel }}/{{ entityNamePascal }}QuerySection';
{% endif %}{% endfor %}

const {{ entityNamePascal }}Page = () => {
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
      <h2 style={ { margin: '0 0 1rem 1rem' } }>{{ pageTitle }}</h2>
      <div
        style={ {
          display: 'grid',
          gridTemplateRows: '{{ gridTemplate.gridTemplateRows }}',
          gridTemplateColumns: '{{ gridTemplate.gridTemplateColumns }}',
          gridTemplateAreas: `{% for area in gridTemplate.gridTemplateAreas %}'{{ area }}'{% if not loop.last %} {% endif %}{% endfor %}`,
          gap: '1rem',
          padding: '0 1rem 1rem 1rem',
        } }
      >
{% for placement in componentPlacements %}      <div style={ { gridArea: '{{ placement.gridArea }}' } }>
{% if placement.componentType == 'form' %}        <{{ entityNamePascal }}Form data={selectedRecord} mode={formMode} onSave={handleSave} onCancel={handleCancel} onNew={handleNew} showForm={showForm} />
{% elif placement.componentType == 'dataTable' %}        <{{ entityNamePascal }}DataTable onRowSelect={handleRowSelect} />
{% elif placement.componentType == 'groupedForm' %}        <{{ entityNamePascal }}GroupedForm />
{% elif placement.componentType == 'filterPanel' %}        <{{ entityNamePascal }}FilterPanel />
{% elif placement.componentType == 'querySection' %}        <{{ entityNamePascal }}QuerySection />
{% endif %}      </div>
{% endfor %}      </div>
    </div>
  );
};

export default {{ entityNamePascal }}Page;
"""
