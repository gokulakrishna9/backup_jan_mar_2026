import React from 'react';
import CandidateInstituteLinkFilterPanel from '../../components/entities/candidateInstituteLink/CandidateInstituteLinkFilterPanel';
import CandidateInstituteLinkDataTable from '../../components/entities/candidateInstituteLink/CandidateInstituteLinkDataTable';

const CandidateInstituteLinkFilterPage = () => {
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
        <CandidateInstituteLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CandidateInstituteLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CandidateInstituteLinkFilterPage;