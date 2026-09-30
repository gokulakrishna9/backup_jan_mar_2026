import React from 'react';
import AiEvaluationParameterFilterPanel from '../../components/entities/aiEvaluationParameter/AiEvaluationParameterFilterPanel';
import AiEvaluationParameterDataTable from '../../components/entities/aiEvaluationParameter/AiEvaluationParameterDataTable';

const AiEvaluationParameterFilterPage = () => {
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
        <AiEvaluationParameterFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiEvaluationParameterDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiEvaluationParameterFilterPage;