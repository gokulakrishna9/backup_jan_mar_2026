import React from 'react';
import JobPostBenefitFilterPanel from '../../components/entities/jobPostBenefit/JobPostBenefitFilterPanel';
import JobPostBenefitDataTable from '../../components/entities/jobPostBenefit/JobPostBenefitDataTable';

const JobPostBenefitFilterPage = () => {
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
        <JobPostBenefitFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <JobPostBenefitDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default JobPostBenefitFilterPage;