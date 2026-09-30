import React from 'react';
import AiMarketTrendPropertyFilterPanel from '../../components/entities/aiMarketTrendProperty/AiMarketTrendPropertyFilterPanel';
import AiMarketTrendPropertyDataTable from '../../components/entities/aiMarketTrendProperty/AiMarketTrendPropertyDataTable';

const AiMarketTrendPropertyFilterPage = () => {
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
        <AiMarketTrendPropertyFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiMarketTrendPropertyDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiMarketTrendPropertyFilterPage;