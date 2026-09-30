import React from 'react';
import MarketTrendDocumentFilterPanel from '../../components/entities/marketTrendDocument/MarketTrendDocumentFilterPanel';
import MarketTrendDocumentDataTable from '../../components/entities/marketTrendDocument/MarketTrendDocumentDataTable';

const MarketTrendDocumentFilterPage = () => {
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
        <MarketTrendDocumentFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <MarketTrendDocumentDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default MarketTrendDocumentFilterPage;