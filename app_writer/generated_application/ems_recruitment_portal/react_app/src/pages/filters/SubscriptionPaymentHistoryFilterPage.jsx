import React from 'react';
import SubscriptionPaymentHistoryFilterPanel from '../../components/entities/subscriptionPaymentHistory/SubscriptionPaymentHistoryFilterPanel';
import SubscriptionPaymentHistoryDataTable from '../../components/entities/subscriptionPaymentHistory/SubscriptionPaymentHistoryDataTable';

const SubscriptionPaymentHistoryFilterPage = () => {
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
        <SubscriptionPaymentHistoryFilterPanel />
      </div>
      <div style={ { gridArea: 'results' } }>
        <SubscriptionPaymentHistoryDataTable onRowSelect={() => {}} />
      </div>
      </div>
    </div>
  );
};

export default SubscriptionPaymentHistoryFilterPage;