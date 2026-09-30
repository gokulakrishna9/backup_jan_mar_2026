import React from 'react';
import InstitutionPropertyFilterPanel from '../../components/entities/institutionProperty/InstitutionPropertyFilterPanel';
import InstitutionPropertyDataTable from '../../components/entities/institutionProperty/InstitutionPropertyDataTable';

const InstitutionPropertyFilterPage = () => {
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
        <InstitutionPropertyFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <InstitutionPropertyDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default InstitutionPropertyFilterPage;