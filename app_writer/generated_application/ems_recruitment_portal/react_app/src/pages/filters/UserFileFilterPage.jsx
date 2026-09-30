import React from 'react';
import UserFileFilterPanel from '../../components/entities/userFile/UserFileFilterPanel';
import UserFileDataTable from '../../components/entities/userFile/UserFileDataTable';

const UserFileFilterPage = () => {
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
        <UserFileFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserFileDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserFileFilterPage;