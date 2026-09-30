import React from 'react';
import MarketTrendJobPostLinkFilterPanel from '../../components/entities/marketTrendJobPostLink/MarketTrendJobPostLinkFilterPanel';
import MarketTrendJobPostLinkDataTable from '../../components/entities/marketTrendJobPostLink/MarketTrendJobPostLinkDataTable';

const MarketTrendJobPostLinkFilterPage = () => {
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
        <MarketTrendJobPostLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <MarketTrendJobPostLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default MarketTrendJobPostLinkFilterPage;