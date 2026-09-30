import React from 'react';
import InstitutionFilterPanel from '../../components/entities/institution/InstitutionFilterPanel';
import InstitutionDataTable from '../../components/entities/institution/InstitutionDataTable';

const InstitutionFilterPage = () => {
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
        <InstitutionFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <InstitutionDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default InstitutionFilterPage;