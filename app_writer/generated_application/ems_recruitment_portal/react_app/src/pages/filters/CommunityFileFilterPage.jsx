import React from 'react';
import CommunityFileFilterPanel from '../../components/entities/communityFile/CommunityFileFilterPanel';
import CommunityFileDataTable from '../../components/entities/communityFile/CommunityFileDataTable';

const CommunityFileFilterPage = () => {
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
        <CommunityFileFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityFileDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityFileFilterPage;