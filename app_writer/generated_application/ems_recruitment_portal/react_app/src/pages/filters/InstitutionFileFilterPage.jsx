import React from 'react';
import InstitutionFileFilterPanel from '../../components/entities/institutionFile/InstitutionFileFilterPanel';
import InstitutionFileDataTable from '../../components/entities/institutionFile/InstitutionFileDataTable';

const InstitutionFileFilterPage = () => {
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
        <InstitutionFileFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <InstitutionFileDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default InstitutionFileFilterPage;