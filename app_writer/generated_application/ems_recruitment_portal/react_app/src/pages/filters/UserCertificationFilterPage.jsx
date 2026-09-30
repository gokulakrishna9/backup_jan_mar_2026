import React from 'react';
import UserCertificationFilterPanel from '../../components/entities/userCertification/UserCertificationFilterPanel';
import UserCertificationDataTable from '../../components/entities/userCertification/UserCertificationDataTable';

const UserCertificationFilterPage = () => {
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
        <UserCertificationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserCertificationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserCertificationFilterPage;