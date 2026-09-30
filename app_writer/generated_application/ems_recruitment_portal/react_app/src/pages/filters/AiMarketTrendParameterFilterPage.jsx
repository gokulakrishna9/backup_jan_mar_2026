import React from 'react';
import AiMarketTrendParameterFilterPanel from '../../components/entities/aiMarketTrendParameter/AiMarketTrendParameterFilterPanel';
import AiMarketTrendParameterDataTable from '../../components/entities/aiMarketTrendParameter/AiMarketTrendParameterDataTable';

const AiMarketTrendParameterFilterPage = () => {
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
        <AiMarketTrendParameterFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiMarketTrendParameterDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiMarketTrendParameterFilterPage;