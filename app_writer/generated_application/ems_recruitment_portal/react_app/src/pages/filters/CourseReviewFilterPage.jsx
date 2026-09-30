import React from 'react';
import CourseReviewFilterPanel from '../../components/entities/courseReview/CourseReviewFilterPanel';
import CourseReviewDataTable from '../../components/entities/courseReview/CourseReviewDataTable';

const CourseReviewFilterPage = () => {
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
        <CourseReviewFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CourseReviewDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CourseReviewFilterPage;