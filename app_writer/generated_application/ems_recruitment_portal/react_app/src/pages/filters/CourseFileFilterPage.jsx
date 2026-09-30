import React from 'react';
import CourseFileFilterPanel from '../../components/entities/courseFile/CourseFileFilterPanel';
import CourseFileDataTable from '../../components/entities/courseFile/CourseFileDataTable';

const CourseFileFilterPage = () => {
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
        <CourseFileFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CourseFileDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CourseFileFilterPage;