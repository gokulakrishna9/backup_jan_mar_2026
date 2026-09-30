import React from 'react';
import UserProfileDocumentFilterPanel from '../../components/entities/userProfileDocument/UserProfileDocumentFilterPanel';
import UserProfileDocumentDataTable from '../../components/entities/userProfileDocument/UserProfileDocumentDataTable';

const UserProfileDocumentFilterPage = () => {
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
        <UserProfileDocumentFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserProfileDocumentDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserProfileDocumentFilterPage;