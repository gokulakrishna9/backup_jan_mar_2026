import React from 'react';
import AiCommunityPostEvaluationFilterPanel from '../../components/entities/aiCommunityPostEvaluation/AiCommunityPostEvaluationFilterPanel';
import AiCommunityPostEvaluationDataTable from '../../components/entities/aiCommunityPostEvaluation/AiCommunityPostEvaluationDataTable';

const AiCommunityPostEvaluationFilterPage = () => {
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
        <AiCommunityPostEvaluationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiCommunityPostEvaluationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiCommunityPostEvaluationFilterPage;