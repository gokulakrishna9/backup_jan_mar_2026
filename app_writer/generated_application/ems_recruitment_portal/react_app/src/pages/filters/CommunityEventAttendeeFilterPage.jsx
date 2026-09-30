import React from 'react';
import CommunityEventAttendeeFilterPanel from '../../components/entities/communityEventAttendee/CommunityEventAttendeeFilterPanel';
import CommunityEventAttendeeDataTable from '../../components/entities/communityEventAttendee/CommunityEventAttendeeDataTable';

const CommunityEventAttendeeFilterPage = () => {
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
        <CommunityEventAttendeeFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <CommunityEventAttendeeDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default CommunityEventAttendeeFilterPage;