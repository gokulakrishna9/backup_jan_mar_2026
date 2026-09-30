import React from 'react';
import InstitutionRankingFilterPanel from '../../components/entities/institutionRanking/InstitutionRankingFilterPanel';
import InstitutionRankingDataTable from '../../components/entities/institutionRanking/InstitutionRankingDataTable';

const InstitutionRankingFilterPage = () => {
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
        <InstitutionRankingFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <InstitutionRankingDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default InstitutionRankingFilterPage;