import React from 'react';
import UserCourseProgressFilterPanel from '../../components/entities/userCourseProgress/UserCourseProgressFilterPanel';
import UserCourseProgressDataTable from '../../components/entities/userCourseProgress/UserCourseProgressDataTable';

const UserCourseProgressFilterPage = () => {
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
        <UserCourseProgressFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserCourseProgressDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserCourseProgressFilterPage;