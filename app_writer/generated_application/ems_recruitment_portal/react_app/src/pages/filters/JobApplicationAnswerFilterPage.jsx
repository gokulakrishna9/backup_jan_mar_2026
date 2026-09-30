import React from 'react';
import JobApplicationAnswerFilterPanel from '../../components/entities/jobApplicationAnswer/JobApplicationAnswerFilterPanel';
import JobApplicationAnswerDataTable from '../../components/entities/jobApplicationAnswer/JobApplicationAnswerDataTable';

const JobApplicationAnswerFilterPage = () => {
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
        <JobApplicationAnswerFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobApplicationAnswerDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobApplicationAnswerFilterPage;