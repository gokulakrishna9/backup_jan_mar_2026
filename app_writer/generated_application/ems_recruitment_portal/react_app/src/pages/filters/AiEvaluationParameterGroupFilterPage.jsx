import React from 'react';
import AiEvaluationParameterGroupFilterPanel from '../../components/entities/aiEvaluationParameterGroup/AiEvaluationParameterGroupFilterPanel';
import AiEvaluationParameterGroupDataTable from '../../components/entities/aiEvaluationParameterGroup/AiEvaluationParameterGroupDataTable';

const AiEvaluationParameterGroupFilterPage = () => {
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
        <AiEvaluationParameterGroupFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiEvaluationParameterGroupDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiEvaluationParameterGroupFilterPage;