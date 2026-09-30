import React from 'react';
import UserJobPostBookmarkFilterPanel from '../../components/entities/userJobPostBookmark/UserJobPostBookmarkFilterPanel';
import UserJobPostBookmarkDataTable from '../../components/entities/userJobPostBookmark/UserJobPostBookmarkDataTable';

const UserJobPostBookmarkFilterPage = () => {
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
        <UserJobPostBookmarkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserJobPostBookmarkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserJobPostBookmarkFilterPage;