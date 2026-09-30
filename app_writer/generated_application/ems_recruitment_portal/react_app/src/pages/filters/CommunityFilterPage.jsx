import React from 'react';
import CommunityFilterPanel from '../../components/entities/community/CommunityFilterPanel';
import CommunityDataTable from '../../components/entities/community/CommunityDataTable';

const CommunityFilterPage = () => {
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
        <CommunityFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityFilterPage;