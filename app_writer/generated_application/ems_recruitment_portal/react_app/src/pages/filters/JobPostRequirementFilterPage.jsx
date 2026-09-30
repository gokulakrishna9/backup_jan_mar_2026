import React from 'react';
import JobPostRequirementFilterPanel from '../../components/entities/jobPostRequirement/JobPostRequirementFilterPanel';
import JobPostRequirementDataTable from '../../components/entities/jobPostRequirement/JobPostRequirementDataTable';

const JobPostRequirementFilterPage = () => {
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
        <JobPostRequirementFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobPostRequirementDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobPostRequirementFilterPage;