import React from 'react';
import UserPropertyFilterPanel from '../../components/entities/userProperty/UserPropertyFilterPanel';
import UserPropertyDataTable from '../../components/entities/userProperty/UserPropertyDataTable';

const UserPropertyFilterPage = () => {
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
        <UserPropertyFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserPropertyDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserPropertyFilterPage;