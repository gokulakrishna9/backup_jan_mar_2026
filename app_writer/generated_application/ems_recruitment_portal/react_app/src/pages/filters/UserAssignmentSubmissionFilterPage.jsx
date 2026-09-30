import React from 'react';
import UserAssignmentSubmissionFilterPanel from '../../components/entities/userAssignmentSubmission/UserAssignmentSubmissionFilterPanel';
import UserAssignmentSubmissionDataTable from '../../components/entities/userAssignmentSubmission/UserAssignmentSubmissionDataTable';

const UserAssignmentSubmissionFilterPage = () => {
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
        <UserAssignmentSubmissionFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserAssignmentSubmissionDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserAssignmentSubmissionFilterPage;