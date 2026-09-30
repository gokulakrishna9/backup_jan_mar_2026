import React from 'react';
import CoursePropertyFilterPanel from '../../components/entities/courseProperty/CoursePropertyFilterPanel';
import CoursePropertyDataTable from '../../components/entities/courseProperty/CoursePropertyDataTable';

const CoursePropertyFilterPage = () => {
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
        <CoursePropertyFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CoursePropertyDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CoursePropertyFilterPage;