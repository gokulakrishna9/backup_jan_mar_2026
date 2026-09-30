import React from 'react';
import MarketTrendCourseLinkFilterPanel from '../../components/entities/marketTrendCourseLink/MarketTrendCourseLinkFilterPanel';
import MarketTrendCourseLinkDataTable from '../../components/entities/marketTrendCourseLink/MarketTrendCourseLinkDataTable';

const MarketTrendCourseLinkFilterPage = () => {
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
        <MarketTrendCourseLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <MarketTrendCourseLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default MarketTrendCourseLinkFilterPage;