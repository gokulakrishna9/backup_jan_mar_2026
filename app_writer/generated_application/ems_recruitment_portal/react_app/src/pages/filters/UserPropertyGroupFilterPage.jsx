import React from 'react';
import UserPropertyGroupFilterPanel from '../../components/entities/userPropertyGroup/UserPropertyGroupFilterPanel';
import UserPropertyGroupDataTable from '../../components/entities/userPropertyGroup/UserPropertyGroupDataTable';

const UserPropertyGroupFilterPage = () => {
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
        <UserPropertyGroupFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserPropertyGroupDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserPropertyGroupFilterPage;