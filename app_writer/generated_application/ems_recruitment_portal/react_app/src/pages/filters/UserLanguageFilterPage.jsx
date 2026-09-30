import React from 'react';
import UserLanguageFilterPanel from '../../components/entities/userLanguage/UserLanguageFilterPanel';
import UserLanguageDataTable from '../../components/entities/userLanguage/UserLanguageDataTable';

const UserLanguageFilterPage = () => {
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
        <UserLanguageFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserLanguageDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserLanguageFilterPage;