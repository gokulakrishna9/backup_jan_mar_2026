import React from 'react';
import InstitutionDepartmentFilterPanel from '../../components/entities/institutionDepartment/InstitutionDepartmentFilterPanel';
import InstitutionDepartmentDataTable from '../../components/entities/institutionDepartment/InstitutionDepartmentDataTable';

const InstitutionDepartmentFilterPage = () => {
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
        <InstitutionDepartmentFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <InstitutionDepartmentDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default InstitutionDepartmentFilterPage;