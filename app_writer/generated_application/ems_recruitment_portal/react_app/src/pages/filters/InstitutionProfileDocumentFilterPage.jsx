import React from 'react';
import InstitutionProfileDocumentFilterPanel from '../../components/entities/institutionProfileDocument/InstitutionProfileDocumentFilterPanel';
import InstitutionProfileDocumentDataTable from '../../components/entities/institutionProfileDocument/InstitutionProfileDocumentDataTable';

const InstitutionProfileDocumentFilterPage = () => {
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
        <InstitutionProfileDocumentFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <InstitutionProfileDocumentDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default InstitutionProfileDocumentFilterPage;