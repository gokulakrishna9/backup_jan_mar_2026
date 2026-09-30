import React from 'react';
import UserRecommendationFilterPanel from '../../components/entities/userRecommendation/UserRecommendationFilterPanel';
import UserRecommendationDataTable from '../../components/entities/userRecommendation/UserRecommendationDataTable';

const UserRecommendationFilterPage = () => {
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
        <UserRecommendationFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserRecommendationDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserRecommendationFilterPage;