import React from 'react';
import PostTagLinkFilterPanel from '../../components/entities/postTagLink/PostTagLinkFilterPanel';
import PostTagLinkDataTable from '../../components/entities/postTagLink/PostTagLinkDataTable';

const PostTagLinkFilterPage = () => {
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
        <PostTagLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <PostTagLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default PostTagLinkFilterPage;