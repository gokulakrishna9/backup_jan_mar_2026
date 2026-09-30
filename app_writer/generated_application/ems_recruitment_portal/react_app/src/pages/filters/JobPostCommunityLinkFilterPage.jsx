import React from 'react';
import JobPostCommunityLinkFilterPanel from '../../components/entities/jobPostCommunityLink/JobPostCommunityLinkFilterPanel';
import JobPostCommunityLinkDataTable from '../../components/entities/jobPostCommunityLink/JobPostCommunityLinkDataTable';

const JobPostCommunityLinkFilterPage = () => {
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
        <JobPostCommunityLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobPostCommunityLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobPostCommunityLinkFilterPage;