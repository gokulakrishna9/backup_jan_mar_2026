import React from 'react';
import CommunityPropertyGroupFilterPanel from '../../components/entities/communityPropertyGroup/CommunityPropertyGroupFilterPanel';
import CommunityPropertyGroupDataTable from '../../components/entities/communityPropertyGroup/CommunityPropertyGroupDataTable';

const CommunityPropertyGroupFilterPage = () => {
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
        <CommunityPropertyGroupFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityPropertyGroupDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityPropertyGroupFilterPage;