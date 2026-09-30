import React from 'react';
import MarketTrendLocationFilterPanel from '../../components/entities/marketTrendLocation/MarketTrendLocationFilterPanel';
import MarketTrendLocationDataTable from '../../components/entities/marketTrendLocation/MarketTrendLocationDataTable';

const MarketTrendLocationFilterPage = () => {
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
        <MarketTrendLocationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <MarketTrendLocationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default MarketTrendLocationFilterPage;