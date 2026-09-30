import React from 'react';
import AiUserProfileEvaluationParameterGroupFilterPanel from '../../components/entities/aiUserProfileEvaluationParameterGroup/AiUserProfileEvaluationParameterGroupFilterPanel';
import AiUserProfileEvaluationParameterGroupDataTable from '../../components/entities/aiUserProfileEvaluationParameterGroup/AiUserProfileEvaluationParameterGroupDataTable';

const AiUserProfileEvaluationParameterGroupFilterPage = () => {
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
        <AiUserProfileEvaluationParameterGroupFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiUserProfileEvaluationParameterGroupDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiUserProfileEvaluationParameterGroupFilterPage;