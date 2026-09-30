import React, { useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Calendar } from 'primereact/calendar';

/**
 * CalendarWrapper — wrapper around PrimeReact Calendar.
 *
 * Props:
 *   reduxActions    — { eventName: actionCreator } mapping for dispatch
 *   reduxSubscriptions — { selectorFn: callbackFn } mapping for store reads
 *   eventHandlers   — { eventName: handlerFn } custom event handlers
 *   style           — { width, height } override
 *   ...rest         — passed through to Calendar
 */
const CalendarWrapper = ({
  reduxActions = {},
  reduxSubscriptions = {},
  eventHandlers = {},
  style = {},
  ...rest
}) => {
  const dispatch = useDispatch();

  // Build event handlers that dispatch Redux actions
  const buildHandler = useCallback(
    (eventName) => (...args) => {
      if (reduxActions[eventName]) {
        dispatch(reduxActions[eventName](...args));
      }
      if (eventHandlers[eventName]) {
        eventHandlers[eventName](...args);
      }
    },
    [dispatch, reduxActions, eventHandlers]
  );

  // Merge event props
  const eventProps = {};
  const allEvents = new Set([
    ...Object.keys(reduxActions),
    ...Object.keys(eventHandlers),
  ]);
  allEvents.forEach((eventName) => {
    eventProps[eventName] = buildHandler(eventName);
  });

  return (
    <Calendar
      style={style}
      {...rest}
      {...eventProps}
    />
  );
};

export default CalendarWrapper;