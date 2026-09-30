import React from 'react';
import UserCourseLinkFilterPanel from '../../components/entities/userCourseLink/UserCourseLinkFilterPanel';
import UserCourseLinkDataTable from '../../components/entities/userCourseLink/UserCourseLinkDataTable';

const UserCourseLinkFilterPage = () => {
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
        <UserCourseLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserCourseLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserCourseLinkFilterPage;