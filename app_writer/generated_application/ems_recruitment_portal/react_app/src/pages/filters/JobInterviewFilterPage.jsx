import React from 'react';
import JobInterviewFilterPanel from '../../components/entities/jobInterview/JobInterviewFilterPanel';
import JobInterviewDataTable from '../../components/entities/jobInterview/JobInterviewDataTable';

const JobInterviewFilterPage = () => {
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
        <JobInterviewFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobInterviewDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobInterviewFilterPage;