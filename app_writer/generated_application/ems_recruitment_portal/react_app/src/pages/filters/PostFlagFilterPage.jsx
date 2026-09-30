import React from 'react';
import PostFlagFilterPanel from '../../components/entities/postFlag/PostFlagFilterPanel';
import PostFlagDataTable from '../../components/entities/postFlag/PostFlagDataTable';

const PostFlagFilterPage = () => {
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
        <PostFlagFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <PostFlagDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default PostFlagFilterPage;