import React from 'react';
import AiUserProfileEvaluationParameterFilterPanel from '../../components/entities/aiUserProfileEvaluationParameter/AiUserProfileEvaluationParameterFilterPanel';
import AiUserProfileEvaluationParameterDataTable from '../../components/entities/aiUserProfileEvaluationParameter/AiUserProfileEvaluationParameterDataTable';

const AiUserProfileEvaluationParameterFilterPage = () => {
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
        <AiUserProfileEvaluationParameterFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiUserProfileEvaluationParameterDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiUserProfileEvaluationParameterFilterPage;