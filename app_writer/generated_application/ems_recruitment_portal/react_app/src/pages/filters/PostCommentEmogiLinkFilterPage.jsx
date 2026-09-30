import React from 'react';
import PostCommentEmogiLinkFilterPanel from '../../components/entities/postCommentEmogiLink/PostCommentEmogiLinkFilterPanel';
import PostCommentEmogiLinkDataTable from '../../components/entities/postCommentEmogiLink/PostCommentEmogiLinkDataTable';

const PostCommentEmogiLinkFilterPage = () => {
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
        <PostCommentEmogiLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <PostCommentEmogiLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default PostCommentEmogiLinkFilterPage;