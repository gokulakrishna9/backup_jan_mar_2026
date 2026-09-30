import React from 'react';
import EmogiPostUserLinkFilterPanel from '../../components/entities/emogiPostUserLink/EmogiPostUserLinkFilterPanel';
import EmogiPostUserLinkDataTable from '../../components/entities/emogiPostUserLink/EmogiPostUserLinkDataTable';

const EmogiPostUserLinkFilterPage = () => {
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
        <EmogiPostUserLinkFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <EmogiPostUserLinkDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default EmogiPostUserLinkFilterPage;