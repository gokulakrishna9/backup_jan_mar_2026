import React from 'react';
import CommunityUserLinkFilterPanel from '../../components/entities/communityUserLink/CommunityUserLinkFilterPanel';
import CommunityUserLinkDataTable from '../../components/entities/communityUserLink/CommunityUserLinkDataTable';

const CommunityUserLinkFilterPage = () => {
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
        <CommunityUserLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityUserLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityUserLinkFilterPage;