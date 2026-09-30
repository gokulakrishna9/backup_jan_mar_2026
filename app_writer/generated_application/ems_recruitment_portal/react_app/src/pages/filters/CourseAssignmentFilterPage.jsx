import React from 'react';
import CourseAssignmentFilterPanel from '../../components/entities/courseAssignment/CourseAssignmentFilterPanel';
import CourseAssignmentDataTable from '../../components/entities/courseAssignment/CourseAssignmentDataTable';

const CourseAssignmentFilterPage = () => {
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
        <CourseAssignmentFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CourseAssignmentDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CourseAssignmentFilterPage;