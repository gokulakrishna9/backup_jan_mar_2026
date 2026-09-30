import React from 'react';
import CommunityPostLinkFilterPanel from '../../components/entities/communityPostLink/CommunityPostLinkFilterPanel';
import CommunityPostLinkDataTable from '../../components/entities/communityPostLink/CommunityPostLinkDataTable';

const CommunityPostLinkFilterPage = () => {
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
        <CommunityPostLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityPostLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityPostLinkFilterPage;