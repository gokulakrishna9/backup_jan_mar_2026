import React from 'react';
import PostAttachmentFilterPanel from '../../components/entities/postAttachment/PostAttachmentFilterPanel';
import PostAttachmentDataTable from '../../components/entities/postAttachment/PostAttachmentDataTable';

const PostAttachmentFilterPage = () => {
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
        <PostAttachmentFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <PostAttachmentDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default PostAttachmentFilterPage;