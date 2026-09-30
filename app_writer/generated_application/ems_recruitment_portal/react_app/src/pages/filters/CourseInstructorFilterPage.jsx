import React from 'react';
import CourseInstructorFilterPanel from '../../components/entities/courseInstructor/CourseInstructorFilterPanel';
import CourseInstructorDataTable from '../../components/entities/courseInstructor/CourseInstructorDataTable';

const CourseInstructorFilterPage = () => {
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
        <CourseInstructorFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CourseInstructorDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CourseInstructorFilterPage;