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
import { createJobApplication } from '../../../store/slices/jobApplicationSlice';
import { updateJobApplication } from '../../../store/slices/jobApplicationSlice';
import logger from '../../../utils/logger';

const JobApplicationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/jobapplications');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      jobPostId: null,
      userId: null,
      coverLetter: '',
      resumeDocumentId: null,
      applicationStatus: '',
      appliedAt: null,
      statusUpdatedAt: null,
      statusUpdatedByUserId: null,
      notes: '',
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
      if (data?.applicationId) {
        await dispatch(updateJobApplication({ id: data.applicationId, data: submitData })).unwrap();
      } else {
        await dispatch(createJobApplication(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('JobApplication save', err);
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
            <label htmlFor="jobPostId">Job Post Id <span className="p-error">*</span></label>
            <Controller name="jobPostId" control={control} rules={ {required: 'Jobpostid is required',} }
              render={({ field: f }) => (
                <InputNumber id="jobPostId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('jobPostId') ? 'p-invalid' : ''} aria-describedby="jobPostId-error" />
              )}
            />
            {getErrorMessage('jobPostId') && <small id="jobPostId-error" className="p-error">{getErrorMessage('jobPostId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="userId">User Id <span className="p-error">*</span></label>
            <Controller name="userId" control={control} rules={ {required: 'Userid is required',} }
              render={({ field: f }) => (
                <InputNumber id="userId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('userId') ? 'p-invalid' : ''} aria-describedby="userId-error" />
              )}
            />
            {getErrorMessage('userId') && <small id="userId-error" className="p-error">{getErrorMessage('userId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="coverLetter">Cover Letter</label>
            <Controller name="coverLetter" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="coverLetter" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('coverLetter') ? 'p-invalid' : ''} aria-describedby="coverLetter-error" />
              )}
            />
            {getErrorMessage('coverLetter') && <small id="coverLetter-error" className="p-error">{getErrorMessage('coverLetter')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="resumeDocumentId">Resume Document Id</label>
            <Controller name="resumeDocumentId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="resumeDocumentId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('resumeDocumentId') ? 'p-invalid' : ''} aria-describedby="resumeDocumentId-error" />
              )}
            />
            {getErrorMessage('resumeDocumentId') && <small id="resumeDocumentId-error" className="p-error">{getErrorMessage('resumeDocumentId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="applicationStatus">Application Status</label>
            <Controller name="applicationStatus" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="applicationStatus" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('applicationStatus') ? 'p-invalid' : ''} aria-describedby="applicationStatus-error" />
              )}
            />
            {getErrorMessage('applicationStatus') && <small id="applicationStatus-error" className="p-error">{getErrorMessage('applicationStatus')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="appliedAt">Applied At</label>
            <Controller name="appliedAt" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="appliedAt" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('appliedAt') ? 'p-invalid' : ''} aria-describedby="appliedAt-error" />
              )}
            />
            {getErrorMessage('appliedAt') && <small id="appliedAt-error" className="p-error">{getErrorMessage('appliedAt')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="statusUpdatedAt">Status Updated At</label>
            <Controller name="statusUpdatedAt" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="statusUpdatedAt" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('statusUpdatedAt') ? 'p-invalid' : ''} aria-describedby="statusUpdatedAt-error" />
              )}
            />
            {getErrorMessage('statusUpdatedAt') && <small id="statusUpdatedAt-error" className="p-error">{getErrorMessage('statusUpdatedAt')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="statusUpdatedByUserId">Status Updated By User Id</label>
            <Controller name="statusUpdatedByUserId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="statusUpdatedByUserId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('statusUpdatedByUserId') ? 'p-invalid' : ''} aria-describedby="statusUpdatedByUserId-error" />
              )}
            />
            {getErrorMessage('statusUpdatedByUserId') && <small id="statusUpdatedByUserId-error" className="p-error">{getErrorMessage('statusUpdatedByUserId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="notes">Notes</label>
            <Controller name="notes" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="notes" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('notes') ? 'p-invalid' : ''} aria-describedby="notes-error" />
              )}
            />
            {getErrorMessage('notes') && <small id="notes-error" className="p-error">{getErrorMessage('notes')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.applicationId && (
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

export default JobApplicationForm;