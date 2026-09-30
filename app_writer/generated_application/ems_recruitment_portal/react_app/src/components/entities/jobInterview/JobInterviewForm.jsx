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
import { createJobInterview } from '../../../store/slices/jobInterviewSlice';
import { updateJobInterview } from '../../../store/slices/jobInterviewSlice';
import logger from '../../../utils/logger';

const JobInterviewForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/jobinterviews');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      applicationId: null,
      interviewType: '',
      interviewRound: null,
      scheduledAt: null,
      durationMinutes: null,
      location: '',
      meetingLink: '',
      interviewerUserId: null,
      status: '',
      feedback: '',
      rating: null,
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
      if (data?.interviewId) {
        await dispatch(updateJobInterview({ id: data.interviewId, data: submitData })).unwrap();
      } else {
        await dispatch(createJobInterview(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('JobInterview save', err);
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
            <label htmlFor="applicationId">Application Id <span className="p-error">*</span></label>
            <Controller name="applicationId" control={control} rules={ {required: 'Applicationid is required',} }
              render={({ field: f }) => (
                <InputNumber id="applicationId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('applicationId') ? 'p-invalid' : ''} aria-describedby="applicationId-error" />
              )}
            />
            {getErrorMessage('applicationId') && <small id="applicationId-error" className="p-error">{getErrorMessage('applicationId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="interviewType">Interview Type</label>
            <Controller name="interviewType" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="interviewType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('interviewType') ? 'p-invalid' : ''} aria-describedby="interviewType-error" />
              )}
            />
            {getErrorMessage('interviewType') && <small id="interviewType-error" className="p-error">{getErrorMessage('interviewType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="interviewRound">Interview Round</label>
            <Controller name="interviewRound" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="interviewRound" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('interviewRound') ? 'p-invalid' : ''} aria-describedby="interviewRound-error" />
              )}
            />
            {getErrorMessage('interviewRound') && <small id="interviewRound-error" className="p-error">{getErrorMessage('interviewRound')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="scheduledAt">Scheduled At <span className="p-error">*</span></label>
            <Controller name="scheduledAt" control={control} rules={ {required: 'Scheduledat is required',} }
              render={({ field: f }) => (
                <Calendar id="scheduledAt" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('scheduledAt') ? 'p-invalid' : ''} aria-describedby="scheduledAt-error" />
              )}
            />
            {getErrorMessage('scheduledAt') && <small id="scheduledAt-error" className="p-error">{getErrorMessage('scheduledAt')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="durationMinutes">Duration Minutes</label>
            <Controller name="durationMinutes" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="durationMinutes" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('durationMinutes') ? 'p-invalid' : ''} aria-describedby="durationMinutes-error" />
              )}
            />
            {getErrorMessage('durationMinutes') && <small id="durationMinutes-error" className="p-error">{getErrorMessage('durationMinutes')}</small>}
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
            <label htmlFor="interviewerUserId">Interviewer User Id</label>
            <Controller name="interviewerUserId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="interviewerUserId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('interviewerUserId') ? 'p-invalid' : ''} aria-describedby="interviewerUserId-error" />
              )}
            />
            {getErrorMessage('interviewerUserId') && <small id="interviewerUserId-error" className="p-error">{getErrorMessage('interviewerUserId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="status">Status</label>
            <Controller name="status" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="status" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('status') ? 'p-invalid' : ''} aria-describedby="status-error" />
              )}
            />
            {getErrorMessage('status') && <small id="status-error" className="p-error">{getErrorMessage('status')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="feedback">Feedback</label>
            <Controller name="feedback" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="feedback" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('feedback') ? 'p-invalid' : ''} aria-describedby="feedback-error" />
              )}
            />
            {getErrorMessage('feedback') && <small id="feedback-error" className="p-error">{getErrorMessage('feedback')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="rating">Rating</label>
            <Controller name="rating" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="rating" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('rating') ? 'p-invalid' : ''} aria-describedby="rating-error" />
              )}
            />
            {getErrorMessage('rating') && <small id="rating-error" className="p-error">{getErrorMessage('rating')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.interviewId && (
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

export default JobInterviewForm;