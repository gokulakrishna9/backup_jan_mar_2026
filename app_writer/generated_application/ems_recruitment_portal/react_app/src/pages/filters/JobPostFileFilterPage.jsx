import React from 'react';
import JobPostFileFilterPanel from '../../components/entities/jobPostFile/JobPostFileFilterPanel';
import JobPostFileDataTable from '../../components/entities/jobPostFile/JobPostFileDataTable';

const JobPostFileFilterPage = () => {
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
        <JobPostFileFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobPostFileDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobPostFileFilterPage;