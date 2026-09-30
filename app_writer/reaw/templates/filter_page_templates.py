"""Jinja2 template for per-entity filter page."""

FILTER_PAGE = """import React from 'react';
import {{ entityNamePascal }}FilterPanel from '../../components/entities/{{ entityNameCamel }}/{{ entityNamePascal }}FilterPanel';
import {{ entityNamePascal }}DataTable from '../../components/entities/{{ entityNameCamel }}/{{ entityNamePascal }}DataTable';

const {{ entityNamePascal }}FilterPage = () => {
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
        padding: '1rem',
      } }
    >
{% for placement in componentPlacements %}      <div style={ { gridArea: '{{ placement.gridArea }}' } }>
{% if placement.componentType == 'filterPanel' %}        <{{ entityNamePascal }}FilterPanel />
{% elif placement.componentType == 'dataTable' %}        <{{ entityNamePascal }}DataTable onRowSelect={() => {}} />
{% endif %}      </div>
{% endfor %}      </div>
    </div>
  );
};

export default {{ entityNamePascal }}FilterPage;
"""
