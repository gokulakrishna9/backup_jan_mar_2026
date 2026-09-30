import React from 'react';
import MarketTrendFileFilterPanel from '../../components/entities/marketTrendFile/MarketTrendFileFilterPanel';
import MarketTrendFileDataTable from '../../components/entities/marketTrendFile/MarketTrendFileDataTable';

const MarketTrendFileFilterPage = () => {
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
        <MarketTrendFileFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <MarketTrendFileDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default MarketTrendFileFilterPage;