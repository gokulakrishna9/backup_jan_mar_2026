import React from 'react';
import CoursePropertyGroupFilterPanel from '../../components/entities/coursePropertyGroup/CoursePropertyGroupFilterPanel';
import CoursePropertyGroupDataTable from '../../components/entities/coursePropertyGroup/CoursePropertyGroupDataTable';

const CoursePropertyGroupFilterPage = () => {
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
        <CoursePropertyGroupFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CoursePropertyGroupDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CoursePropertyGroupFilterPage;