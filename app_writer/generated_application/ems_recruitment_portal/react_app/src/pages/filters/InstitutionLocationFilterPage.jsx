import React from 'react';
import InstitutionLocationFilterPanel from '../../components/entities/institutionLocation/InstitutionLocationFilterPanel';
import InstitutionLocationDataTable from '../../components/entities/institutionLocation/InstitutionLocationDataTable';

const InstitutionLocationFilterPage = () => {
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
        <InstitutionLocationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <InstitutionLocationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default InstitutionLocationFilterPage;