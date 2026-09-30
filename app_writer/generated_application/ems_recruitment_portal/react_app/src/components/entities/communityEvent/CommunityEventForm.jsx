import React, { useState, useEffect, useRef } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { useDispatch } from 'react-redux';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { InputTextarea } from 'primereact/inputtextarea';
import { Calendar } from 'primereact/calendar';
import { Checkbox } from 'primereact/checkbox';
import { Dropdown } from 'primereact/dropdown';
import { AutoComplete } from 'primereact/autocomplete';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';
import { usePermissions } from '../../../hooks/usePermissions';
import { createCommunityEvent } from '../../../store/slices/communityEventSlice';
import { updateCommunityEvent } from '../../../store/slices/communityEventSlice';
import logger from '../../../utils/logger';

const CommunityEventForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/communityevents');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      communityId: null,
      eventTitle: '',
      description: '',
      eventType: '',
      startDatetime: null,
      endDatetime: null,
      location: '',
      meetingLink: '',
      maxAttendees: null,
      organizerUserId: null,
    },
  });

  useEffect(() => {
    if (data) {
      reset({ ...data });
    }
  }, [data, reset]);

  const onSubmit = async (formData) => {
    const submitData = { ...formData };
    try {
      if (data?.eventId) {
        await dispatch(updateCommunityEvent({ id: data.eventId, data: submitData })).unwrap();
      } else {
        await dispatch(createCommunityEvent(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CommunityEvent save', err);
      toast.current?.show({ severity: 'error', summary: 'Error', detail: String(err), life: 5000 });
    }
  };

  const isDisabled = !editMode;

  const colsLg = 3;
  const colsMd = 2;
  const colsSm = 1;
  const fullWidthTypes = ["InputTextarea"];


  const getColClass = (componentType) => {
    if (fullWidthTypes.includes(componentType)) {
      return 'col-12';
    }
    return `col-12 md:col-${12 / colsMd} lg:col-${12 / colsLg}`;
  };

  const getErrorMessage = (name) => errors[name]?.message;

  return (
    <div>
      <Toast ref={toast} />
      <div className="flex justify-content-end gap-2 mb-3">
        {!editMode && canCreate && (
          <Button label="New" icon="pi pi-plus" className="p-button-success p-button-sm p-button-sm" onClick={() => { reset({}); setEditMode(true); if (onNew) onNew(); }} />
        )}
      </div>
      {showForm && (
      <form onSubmit={handleSubmit(onSubmit)}>
      <div className="p-fluid">
      <div className="grid">
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="communityId">Community Id <span className="p-error">*</span></label>
            <Controller name="communityId" control={control} rules={ {required: 'Communityid is required',} }
              render={({ field: f }) => (
                <InputNumber id="communityId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('communityId') ? 'p-invalid' : ''} aria-describedby="communityId-error" />
              )}
            />
            {getErrorMessage('communityId') && <small id="communityId-error" className="p-error">{getErrorMessage('communityId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="eventTitle">Event Title <span className="p-error">*</span></label>
            <Controller name="eventTitle" control={control} rules={ {required: 'Eventtitle is required',maxLength: { value: 255, message: 'Eventtitle cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="eventTitle" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('eventTitle') ? 'p-invalid' : ''} aria-describedby="eventTitle-error" />
              )}
            />
            {getErrorMessage('eventTitle') && <small id="eventTitle-error" className="p-error">{getErrorMessage('eventTitle')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="description">Description</label>
            <Controller name="description" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="description" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('description') ? 'p-invalid' : ''} aria-describedby="description-error" />
              )}
            />
            {getErrorMessage('description') && <small id="description-error" className="p-error">{getErrorMessage('description')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="eventType">Event Type</label>
            <Controller name="eventType" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="eventType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('eventType') ? 'p-invalid' : ''} aria-describedby="eventType-error" />
              )}
            />
            {getErrorMessage('eventType') && <small id="eventType-error" className="p-error">{getErrorMessage('eventType')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="startDatetime">Start Datetime <span className="p-error">*</span></label>
            <Controller name="startDatetime" control={control} rules={ {required: 'Startdatetime is required',} }
              render={({ field: f }) => (
                <Calendar id="startDatetime" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('startDatetime') ? 'p-invalid' : ''} aria-describedby="startDatetime-error" />
              )}
            />
            {getErrorMessage('startDatetime') && <small id="startDatetime-error" className="p-error">{getErrorMessage('startDatetime')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="endDatetime">End Datetime <span className="p-error">*</span></label>
            <Controller name="endDatetime" control={control} rules={ {required: 'Enddatetime is required',} }
              render={({ field: f }) => (
                <Calendar id="endDatetime" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('endDatetime') ? 'p-invalid' : ''} aria-describedby="endDatetime-error" />
              )}
            />
            {getErrorMessage('endDatetime') && <small id="endDatetime-error" className="p-error">{getErrorMessage('endDatetime')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="location">Location</label>
            <Controller name="location" control={control} rules={ {maxLength: { value: 255, message: 'Location cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="location" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('location') ? 'p-invalid' : ''} aria-describedby="location-error" />
              )}
            />
            {getErrorMessage('location') && <small id="location-error" className="p-error">{getErrorMessage('location')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="meetingLink">Meeting Link</label>
            <Controller name="meetingLink" control={control} rules={ {maxLength: { value: 500, message: 'Meetinglink cannot exceed 500 characters' },} }
              render={({ field: f }) => (
                <InputText id="meetingLink" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('meetingLink') ? 'p-invalid' : ''} aria-describedby="meetingLink-error" />
              )}
            />
            {getErrorMessage('meetingLink') && <small id="meetingLink-error" className="p-error">{getErrorMessage('meetingLink')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="maxAttendees">Max Attendees</label>
            <Controller name="maxAttendees" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="maxAttendees" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('maxAttendees') ? 'p-invalid' : ''} aria-describedby="maxAttendees-error" />
              )}
            />
            {getErrorMessage('maxAttendees') && <small id="maxAttendees-error" className="p-error">{getErrorMessage('maxAttendees')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="organizerUserId">Organizer User Id <span className="p-error">*</span></label>
            <Controller name="organizerUserId" control={control} rules={ {required: 'Organizeruserid is required',} }
              render={({ field: f }) => (
                <InputNumber id="organizerUserId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('organizerUserId') ? 'p-invalid' : ''} aria-describedby="organizerUserId-error" />
              )}
            />
            {getErrorMessage('organizerUserId') && <small id="organizerUserId-error" className="p-error">{getErrorMessage('organizerUserId')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.eventId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
        )}
        {editMode && (
          <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default CommunityEventForm;