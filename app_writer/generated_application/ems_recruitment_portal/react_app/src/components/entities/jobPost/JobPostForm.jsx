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
import { createJobPost } from '../../../store/slices/jobPostSlice';
import { updateJobPost } from '../../../store/slices/jobPostSlice';
import logger from '../../../utils/logger';

const JobPostForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/jobposts');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      jobPostSubject: '',
      jobPostDescription: '',
      institutionId: null,
      location: '',
      salaryRange: '',
      postedOn: null,
      expiresOn: null,
      isActive: null,
      isEntity: null,
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
      if (data?.jobPostId) {
        await dispatch(updateJobPost({ id: data.jobPostId, data: submitData })).unwrap();
      } else {
        await dispatch(createJobPost(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('JobPost save', err);
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="jobPostSubject">Job Post Subject <span className="p-error">*</span></label>
            <Controller name="jobPostSubject" control={control} rules={ {required: 'Jobpostsubject is required',maxLength: { value: 255, message: 'Jobpostsubject cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="jobPostSubject" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('jobPostSubject') ? 'p-invalid' : ''} aria-describedby="jobPostSubject-error" />
              )}
            />
            {getErrorMessage('jobPostSubject') && <small id="jobPostSubject-error" className="p-error">{getErrorMessage('jobPostSubject')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="jobPostDescription">Job Post Description</label>
            <Controller name="jobPostDescription" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="jobPostDescription" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('jobPostDescription') ? 'p-invalid' : ''} aria-describedby="jobPostDescription-error" />
              )}
            />
            {getErrorMessage('jobPostDescription') && <small id="jobPostDescription-error" className="p-error">{getErrorMessage('jobPostDescription')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="institutionId">Institution Id</label>
            <Controller name="institutionId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="institutionId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('institutionId') ? 'p-invalid' : ''} aria-describedby="institutionId-error" />
              )}
            />
            {getErrorMessage('institutionId') && <small id="institutionId-error" className="p-error">{getErrorMessage('institutionId')}</small>}
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
            <label htmlFor="salaryRange">Salary Range</label>
            <Controller name="salaryRange" control={control} rules={ {maxLength: { value: 100, message: 'Salaryrange cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="salaryRange" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('salaryRange') ? 'p-invalid' : ''} aria-describedby="salaryRange-error" />
              )}
            />
            {getErrorMessage('salaryRange') && <small id="salaryRange-error" className="p-error">{getErrorMessage('salaryRange')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="postedOn">Posted On</label>
            <Controller name="postedOn" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="postedOn" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('postedOn') ? 'p-invalid' : ''} aria-describedby="postedOn-error" />
              )}
            />
            {getErrorMessage('postedOn') && <small id="postedOn-error" className="p-error">{getErrorMessage('postedOn')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="expiresOn">Expires On</label>
            <Controller name="expiresOn" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="expiresOn" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('expiresOn') ? 'p-invalid' : ''} aria-describedby="expiresOn-error" />
              )}
            />
            {getErrorMessage('expiresOn') && <small id="expiresOn-error" className="p-error">{getErrorMessage('expiresOn')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isActive">Is Active</label>
            <Controller name="isActive" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isActive" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isActive') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isActive') && <small id="isActive-error" className="p-error">{getErrorMessage('isActive')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isEntity">Is Entity</label>
            <Controller name="isEntity" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isEntity" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isEntity') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isEntity') && <small id="isEntity-error" className="p-error">{getErrorMessage('isEntity')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.jobPostId && (
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

export default JobPostForm;