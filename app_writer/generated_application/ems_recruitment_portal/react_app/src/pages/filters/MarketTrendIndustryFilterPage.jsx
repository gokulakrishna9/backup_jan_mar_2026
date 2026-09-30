import React from 'react';
import MarketTrendIndustryFilterPanel from '../../components/entities/marketTrendIndustry/MarketTrendIndustryFilterPanel';
import MarketTrendIndustryDataTable from '../../components/entities/marketTrendIndustry/MarketTrendIndustryDataTable';

const MarketTrendIndustryFilterPage = () => {
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
        <MarketTrendIndustryFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <MarketTrendIndustryDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default MarketTrendIndustryFilterPage;