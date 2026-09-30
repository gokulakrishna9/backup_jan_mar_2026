import React from 'react';
import AiUserProfileEvaluationFilterPanel from '../../components/entities/aiUserProfileEvaluation/AiUserProfileEvaluationFilterPanel';
import AiUserProfileEvaluationDataTable from '../../components/entities/aiUserProfileEvaluation/AiUserProfileEvaluationDataTable';

const AiUserProfileEvaluationFilterPage = () => {
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
        <AiUserProfileEvaluationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiUserProfileEvaluationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiUserProfileEvaluationFilterPage;