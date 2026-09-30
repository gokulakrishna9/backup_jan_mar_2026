import React from 'react';
import JobPostDocumentFilterPanel from '../../components/entities/jobPostDocument/JobPostDocumentFilterPanel';
import JobPostDocumentDataTable from '../../components/entities/jobPostDocument/JobPostDocumentDataTable';

const JobPostDocumentFilterPage = () => {
  return (
    <div>
      <h2 style={ { margin: '0 0 1rem 1rem' } }></h2>
      <div
      style={ {
        display: 'grid',
        gridTemplateRows: 'auto 1fr',
        gridTemplateColumns: '1fr',
        gridTemplateAreas: `'filters' 'results'`,
        gap: '1rem',
        padding: '1rem',
      } }
    >
      <div style={ { gridArea: 'filters' } }>
        <JobPostDocumentFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobPostDocumentDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobPostDocumentFilterPage;