import React from 'react';
import CourseLessonFilterPanel from '../../components/entities/courseLesson/CourseLessonFilterPanel';
import CourseLessonDataTable from '../../components/entities/courseLesson/CourseLessonDataTable';

const CourseLessonFilterPage = () => {
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
        <CourseLessonFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CourseLessonDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CourseLessonFilterPage;