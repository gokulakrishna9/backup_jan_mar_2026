import React from 'react';
import UserEducationFilterPanel from '../../components/entities/userEducation/UserEducationFilterPanel';
import UserEducationDataTable from '../../components/entities/userEducation/UserEducationDataTable';

const UserEducationFilterPage = () => {
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
        <UserEducationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserEducationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserEducationFilterPage;