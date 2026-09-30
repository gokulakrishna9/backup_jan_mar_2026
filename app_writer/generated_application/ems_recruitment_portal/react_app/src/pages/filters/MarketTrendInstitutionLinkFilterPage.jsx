import React from 'react';
import MarketTrendInstitutionLinkFilterPanel from '../../components/entities/marketTrendInstitutionLink/MarketTrendInstitutionLinkFilterPanel';
import MarketTrendInstitutionLinkDataTable from '../../components/entities/marketTrendInstitutionLink/MarketTrendInstitutionLinkDataTable';

const MarketTrendInstitutionLinkFilterPage = () => {
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
        <MarketTrendInstitutionLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <MarketTrendInstitutionLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default MarketTrendInstitutionLinkFilterPage;