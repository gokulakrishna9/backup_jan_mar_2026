import React from 'react';
import JobPostQuestionFilterPanel from '../../components/entities/jobPostQuestion/JobPostQuestionFilterPanel';
import JobPostQuestionDataTable from '../../components/entities/jobPostQuestion/JobPostQuestionDataTable';

const JobPostQuestionFilterPage = () => {
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
        <JobPostQuestionFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobPostQuestionDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobPostQuestionFilterPage;