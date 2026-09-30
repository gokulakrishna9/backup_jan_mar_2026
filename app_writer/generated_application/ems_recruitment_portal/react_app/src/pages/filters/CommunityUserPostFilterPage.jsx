import React from 'react';
import CommunityUserPostFilterPanel from '../../components/entities/communityUserPost/CommunityUserPostFilterPanel';
import CommunityUserPostDataTable from '../../components/entities/communityUserPost/CommunityUserPostDataTable';

const CommunityUserPostFilterPage = () => {
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
        <CommunityUserPostFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityUserPostDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityUserPostFilterPage;