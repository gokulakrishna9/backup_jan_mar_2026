import React from 'react';
import UserWorkExperienceFilterPanel from '../../components/entities/userWorkExperience/UserWorkExperienceFilterPanel';
import UserWorkExperienceDataTable from '../../components/entities/userWorkExperience/UserWorkExperienceDataTable';

const UserWorkExperienceFilterPage = () => {
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
        <UserWorkExperienceFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserWorkExperienceDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserWorkExperienceFilterPage;