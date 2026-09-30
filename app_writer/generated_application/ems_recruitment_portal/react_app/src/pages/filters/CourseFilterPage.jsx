import React from 'react';
import CourseFilterPanel from '../../components/entities/course/CourseFilterPanel';
import CourseDataTable from '../../components/entities/course/CourseDataTable';

const CourseFilterPage = () => {
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
        <CourseFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CourseDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CourseFilterPage;