import React from 'react';
import JobApplicationFilterPanel from '../../components/entities/jobApplication/JobApplicationFilterPanel';
import JobApplicationDataTable from '../../components/entities/jobApplication/JobApplicationDataTable';

const JobApplicationFilterPage = () => {
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
        <JobApplicationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobApplicationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobApplicationFilterPage;