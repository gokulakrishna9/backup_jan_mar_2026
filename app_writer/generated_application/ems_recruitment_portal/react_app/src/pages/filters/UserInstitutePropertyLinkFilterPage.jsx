import React from 'react';
import UserInstitutePropertyLinkFilterPanel from '../../components/entities/userInstitutePropertyLink/UserInstitutePropertyLinkFilterPanel';
import UserInstitutePropertyLinkDataTable from '../../components/entities/userInstitutePropertyLink/UserInstitutePropertyLinkDataTable';

const UserInstitutePropertyLinkFilterPage = () => {
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
        <UserInstitutePropertyLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserInstitutePropertyLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserInstitutePropertyLinkFilterPage;