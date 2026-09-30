import React from 'react';
import CourseDocumentFilterPanel from '../../components/entities/courseDocument/CourseDocumentFilterPanel';
import CourseDocumentDataTable from '../../components/entities/courseDocument/CourseDocumentDataTable';

const CourseDocumentFilterPage = () => {
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
        <CourseDocumentFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CourseDocumentDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CourseDocumentFilterPage;