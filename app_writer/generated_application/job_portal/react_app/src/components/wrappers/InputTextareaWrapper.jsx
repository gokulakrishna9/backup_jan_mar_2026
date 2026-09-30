import React, { useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { InputTextarea } from 'primereact/inputtextarea';

/**
 * InputTextareaWrapper — wrapper around PrimeReact InputTextarea.
 *
 * Props:
 *   reduxActions    — { eventName: actionCreator } mapping for dispatch
 *   reduxSubscriptions — { selectorFn: callbackFn } mapping for store reads
 *   eventHandlers   — { eventName: handlerFn } custom event handlers
 *   style           — { width, height } override
 *   ...rest         — passed through to InputTextarea
 */
const InputTextareaWrapper = ({
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
    <InputTextarea
      style={style}
      {...rest}
      {...eventProps}
    />
  );
};

export default InputTextareaWrapper;