import React from 'react';
import InstitutionAccreditationFilterPanel from '../../components/entities/institutionAccreditation/InstitutionAccreditationFilterPanel';
import InstitutionAccreditationDataTable from '../../components/entities/institutionAccreditation/InstitutionAccreditationDataTable';

const InstitutionAccreditationFilterPage = () => {
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
        <InstitutionAccreditationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <InstitutionAccreditationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default InstitutionAccreditationFilterPage;