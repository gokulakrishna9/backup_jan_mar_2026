import React from 'react';
import AiMarketTrendParameterGroupFilterPanel from '../../components/entities/aiMarketTrendParameterGroup/AiMarketTrendParameterGroupFilterPanel';
import AiMarketTrendParameterGroupDataTable from '../../components/entities/aiMarketTrendParameterGroup/AiMarketTrendParameterGroupDataTable';

const AiMarketTrendParameterGroupFilterPage = () => {
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
        <AiMarketTrendParameterGroupFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiMarketTrendParameterGroupDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiMarketTrendParameterGroupFilterPage;