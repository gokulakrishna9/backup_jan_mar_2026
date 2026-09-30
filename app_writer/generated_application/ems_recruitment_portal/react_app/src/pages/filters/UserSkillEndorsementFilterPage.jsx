import React from 'react';
import UserSkillEndorsementFilterPanel from '../../components/entities/userSkillEndorsement/UserSkillEndorsementFilterPanel';
import UserSkillEndorsementDataTable from '../../components/entities/userSkillEndorsement/UserSkillEndorsementDataTable';

const UserSkillEndorsementFilterPage = () => {
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
        <UserSkillEndorsementFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserSkillEndorsementDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserSkillEndorsementFilterPage;