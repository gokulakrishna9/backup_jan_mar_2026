import React from 'react';
import CommunityPropertyFilterPanel from '../../components/entities/communityProperty/CommunityPropertyFilterPanel';
import CommunityPropertyDataTable from '../../components/entities/communityProperty/CommunityPropertyDataTable';

const CommunityPropertyFilterPage = () => {
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
        <CommunityPropertyFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityPropertyDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityPropertyFilterPage;