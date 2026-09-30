import React from 'react';
import CourseModuleFilterPanel from '../../components/entities/courseModule/CourseModuleFilterPanel';
import CourseModuleDataTable from '../../components/entities/courseModule/CourseModuleDataTable';

const CourseModuleFilterPage = () => {
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
        <CourseModuleFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CourseModuleDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CourseModuleFilterPage;