import React from 'react';
import MarketTrendSkillDemandFilterPanel from '../../components/entities/marketTrendSkillDemand/MarketTrendSkillDemandFilterPanel';
import MarketTrendSkillDemandDataTable from '../../components/entities/marketTrendSkillDemand/MarketTrendSkillDemandDataTable';

const MarketTrendSkillDemandFilterPage = () => {
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
        <MarketTrendSkillDemandFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <MarketTrendSkillDemandDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default MarketTrendSkillDemandFilterPage;