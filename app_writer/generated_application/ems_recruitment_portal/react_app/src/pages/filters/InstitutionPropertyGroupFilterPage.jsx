import React from 'react';
import InstitutionPropertyGroupFilterPanel from '../../components/entities/institutionPropertyGroup/InstitutionPropertyGroupFilterPanel';
import InstitutionPropertyGroupDataTable from '../../components/entities/institutionPropertyGroup/InstitutionPropertyGroupDataTable';

const InstitutionPropertyGroupFilterPage = () => {
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
        <InstitutionPropertyGroupFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <InstitutionPropertyGroupDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default InstitutionPropertyGroupFilterPage;