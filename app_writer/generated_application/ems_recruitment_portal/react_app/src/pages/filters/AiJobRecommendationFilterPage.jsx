import React from 'react';
import AiJobRecommendationFilterPanel from '../../components/entities/aiJobRecommendation/AiJobRecommendationFilterPanel';
import AiJobRecommendationDataTable from '../../components/entities/aiJobRecommendation/AiJobRecommendationDataTable';

const AiJobRecommendationFilterPage = () => {
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
        <AiJobRecommendationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiJobRecommendationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiJobRecommendationFilterPage;