import React from 'react';
import UserCourseWishlistFilterPanel from '../../components/entities/userCourseWishlist/UserCourseWishlistFilterPanel';
import UserCourseWishlistDataTable from '../../components/entities/userCourseWishlist/UserCourseWishlistDataTable';

const UserCourseWishlistFilterPage = () => {
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
        <UserCourseWishlistFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserCourseWishlistDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserCourseWishlistFilterPage;