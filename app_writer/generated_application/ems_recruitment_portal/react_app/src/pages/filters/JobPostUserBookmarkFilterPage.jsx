import React from 'react';
import JobPostUserBookmarkFilterPanel from '../../components/entities/jobPostUserBookmark/JobPostUserBookmarkFilterPanel';
import JobPostUserBookmarkDataTable from '../../components/entities/jobPostUserBookmark/JobPostUserBookmarkDataTable';

const JobPostUserBookmarkFilterPage = () => {
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
        <JobPostUserBookmarkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobPostUserBookmarkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobPostUserBookmarkFilterPage;