import React, { useState } from 'react';
import JobPostUserBookmarkQuerySection from '../../components/entities/jobPostUserBookmark/JobPostUserBookmarkQuerySection';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

const JobPostUserBookmarkQueryPage = () => {
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
      <h2 style={ { margin: '0 0 1rem 1rem' } }></h2>
      <div
        style={ {
          display: 'grid',
          gridTemplateRows: 'auto 1fr',
          gridTemplateColumns: '1fr',
          gridTemplateAreas: `'query' 'results'`,
          gap: '1rem',
          padding: '0 1rem 1rem 1rem',
        } }
      >
      <div style={ { gridArea: 'query' } }>
        <JobPostUserBookmarkQuerySection onResults={handleResults} />
      </div>
      <div style={ { gridArea: 'results' } }>
        <DataTable value={results} responsiveLayout="scroll">
          {columns.map((col) => (
            <Column key={col.field} field={col.field} header={col.header} />
          ))}
        </DataTable>
      </div>
      </div>
    </div>
  );
};

export default JobPostUserBookmarkQueryPage;