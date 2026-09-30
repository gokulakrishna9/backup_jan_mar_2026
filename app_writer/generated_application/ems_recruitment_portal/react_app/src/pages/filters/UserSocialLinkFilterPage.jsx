import React from 'react';
import UserSocialLinkFilterPanel from '../../components/entities/userSocialLink/UserSocialLinkFilterPanel';
import UserSocialLinkDataTable from '../../components/entities/userSocialLink/UserSocialLinkDataTable';

const UserSocialLinkFilterPage = () => {
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
        <UserSocialLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserSocialLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserSocialLinkFilterPage;