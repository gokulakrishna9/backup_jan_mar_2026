import React from 'react';
import UserCoursePurchaseFilterPanel from '../../components/entities/userCoursePurchase/UserCoursePurchaseFilterPanel';
import UserCoursePurchaseDataTable from '../../components/entities/userCoursePurchase/UserCoursePurchaseDataTable';

const UserCoursePurchaseFilterPage = () => {
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
        <UserCoursePurchaseFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserCoursePurchaseDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserCoursePurchaseFilterPage;