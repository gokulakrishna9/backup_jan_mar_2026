import React from 'react';
import CourseDocumentGroupFilterPanel from '../../components/entities/courseDocumentGroup/CourseDocumentGroupFilterPanel';
import CourseDocumentGroupDataTable from '../../components/entities/courseDocumentGroup/CourseDocumentGroupDataTable';

const CourseDocumentGroupFilterPage = () => {
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
        <CourseDocumentGroupFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CourseDocumentGroupDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CourseDocumentGroupFilterPage;