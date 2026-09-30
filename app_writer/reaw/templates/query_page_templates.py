"""Jinja2 template for per-entity query page."""

QUERY_PAGE = """import React, { useState } from 'react';
import {{ entityNamePascal }}QuerySection from '../../components/entities/{{ entityNameCamel }}/{{ entityNamePascal }}QuerySection';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

const {{ entityNamePascal }}QueryPage = () => {
  const [results, setResults] = useState([]);
  const [columns, setColumns] = useState([]);

  const handleResults = (data) => {
    const items = data.content || data || [];
    setResults(items);
    if (items.length > 0) {
      setColumns(Object.keys(items[0]).map((key) => ({ field: key, header: key })));
    }
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
{% if placement.componentType == 'querySection' %}        <{{ entityNamePascal }}QuerySection onResults={handleResults} />
{% elif placement.componentType == 'dataTable' %}        <DataTable value={results} responsiveLayout="scroll">
          {columns.map((col) => (
            <Column key={col.field} field={col.field} header={col.header} />
          ))}
        </DataTable>
{% endif %}      </div>
{% endfor %}      </div>
    </div>
  );
};

export default {{ entityNamePascal }}QueryPage;
"""
