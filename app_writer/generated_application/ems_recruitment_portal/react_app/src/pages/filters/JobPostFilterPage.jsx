import React from 'react';
import JobPostFilterPanel from '../../components/entities/jobPost/JobPostFilterPanel';
import JobPostDataTable from '../../components/entities/jobPost/JobPostDataTable';

const JobPostFilterPage = () => {
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
        <JobPostFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobPostDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobPostFilterPage;