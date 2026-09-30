import React from 'react';
import UserSkillFilterPanel from '../../components/entities/userSkill/UserSkillFilterPanel';
import UserSkillDataTable from '../../components/entities/userSkill/UserSkillDataTable';

const UserSkillFilterPage = () => {
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
        <UserSkillFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <UserSkillDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default UserSkillFilterPage;