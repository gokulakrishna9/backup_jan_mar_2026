import React from 'react';
import AiInstitutionProfileEvaluationFilterPanel from '../../components/entities/aiInstitutionProfileEvaluation/AiInstitutionProfileEvaluationFilterPanel';
import AiInstitutionProfileEvaluationDataTable from '../../components/entities/aiInstitutionProfileEvaluation/AiInstitutionProfileEvaluationDataTable';

const AiInstitutionProfileEvaluationFilterPage = () => {
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
        <AiInstitutionProfileEvaluationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <AiInstitutionProfileEvaluationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default AiInstitutionProfileEvaluationFilterPage;