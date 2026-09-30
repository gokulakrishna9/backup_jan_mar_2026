import React from 'react';
import UserFilterPanel from '../../components/entities/user/UserFilterPanel';
import UserDataTable from '../../components/entities/user/UserDataTable';

const UserFilterPage = () => {
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
        <UserFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserFilterPage;