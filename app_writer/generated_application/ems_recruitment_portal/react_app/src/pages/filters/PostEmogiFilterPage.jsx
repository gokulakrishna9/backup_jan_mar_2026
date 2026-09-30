import React from 'react';
import PostEmogiFilterPanel from '../../components/entities/postEmogi/PostEmogiFilterPanel';
import PostEmogiDataTable from '../../components/entities/postEmogi/PostEmogiDataTable';

const PostEmogiFilterPage = () => {
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
        <PostEmogiFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <PostEmogiDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default PostEmogiFilterPage;