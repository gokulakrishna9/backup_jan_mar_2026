import React from 'react';
import CommunityPropertyUserLinkFilterPanel from '../../components/entities/communityPropertyUserLink/CommunityPropertyUserLinkFilterPanel';
import CommunityPropertyUserLinkDataTable from '../../components/entities/communityPropertyUserLink/CommunityPropertyUserLinkDataTable';

const CommunityPropertyUserLinkFilterPage = () => {
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
        <CommunityPropertyUserLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityPropertyUserLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityPropertyUserLinkFilterPage;