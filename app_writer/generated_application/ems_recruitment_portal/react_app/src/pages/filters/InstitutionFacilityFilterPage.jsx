import React from 'react';
import InstitutionFacilityFilterPanel from '../../components/entities/institutionFacility/InstitutionFacilityFilterPanel';
import InstitutionFacilityDataTable from '../../components/entities/institutionFacility/InstitutionFacilityDataTable';

const InstitutionFacilityFilterPage = () => {
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
        <InstitutionFacilityFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <InstitutionFacilityDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default InstitutionFacilityFilterPage;