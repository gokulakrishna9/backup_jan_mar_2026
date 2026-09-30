import React from 'react';
import PostCommentFilterPanel from '../../components/entities/postComment/PostCommentFilterPanel';
import PostCommentDataTable from '../../components/entities/postComment/PostCommentDataTable';

const PostCommentFilterPage = () => {
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
        <PostCommentFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <PostCommentDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default PostCommentFilterPage;