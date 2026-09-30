import React from 'react';
import CommunityRuleFilterPanel from '../../components/entities/communityRule/CommunityRuleFilterPanel';
import CommunityRuleDataTable from '../../components/entities/communityRule/CommunityRuleDataTable';

const CommunityRuleFilterPage = () => {
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
        <CommunityRuleFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityRuleDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityRuleFilterPage;