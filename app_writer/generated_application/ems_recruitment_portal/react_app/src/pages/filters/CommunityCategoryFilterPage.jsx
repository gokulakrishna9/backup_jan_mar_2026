import React from 'react';
import CommunityCategoryFilterPanel from '../../components/entities/communityCategory/CommunityCategoryFilterPanel';
import CommunityCategoryDataTable from '../../components/entities/communityCategory/CommunityCategoryDataTable';

const CommunityCategoryFilterPage = () => {
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
        <CommunityCategoryFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityCategoryDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityCategoryFilterPage;