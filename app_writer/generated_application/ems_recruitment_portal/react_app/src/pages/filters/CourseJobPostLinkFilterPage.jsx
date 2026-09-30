import React from 'react';
import CourseJobPostLinkFilterPanel from '../../components/entities/courseJobPostLink/CourseJobPostLinkFilterPanel';
import CourseJobPostLinkDataTable from '../../components/entities/courseJobPostLink/CourseJobPostLinkDataTable';

const CourseJobPostLinkFilterPage = () => {
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
        <CourseJobPostLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CourseJobPostLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CourseJobPostLinkFilterPage;