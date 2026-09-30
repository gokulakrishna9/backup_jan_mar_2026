import React from 'react';
import PostTagFilterPanel from '../../components/entities/postTag/PostTagFilterPanel';
import PostTagDataTable from '../../components/entities/postTag/PostTagDataTable';

const PostTagFilterPage = () => {
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
        <PostTagFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <PostTagDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default PostTagFilterPage;