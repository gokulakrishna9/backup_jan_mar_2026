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
import { createJobPosting } from '../../../store/slices/jobPostingSlice';
import { updateJobPosting } from '../../../store/slices/jobPostingSlice';
import logger from '../../../utils/logger';

const JobPostingForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/job_postings');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      title: '',
      description: '',
      location: '',
      salarymin: null,
      salarymax: null,
      jobtype: '',
      isactive: null,
    },
  });

  useEffect(() => {
    if (data) {
      reset({ ...data });
    }
  }, [data, reset]);

  useEffect(() => {
    setEditMode(mode === 'create' || mode === 'edit');
  }, [mode]);



  const onSubmit = async (formData) => {
    const submitData = { ...formData };
    try {
      if (data?.jobPostingId) {
        await dispatch(updateJobPosting({ id: data.jobPostingId, data: submitData })).unwrap();
      } else {
        await dispatch(createJobPosting(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('JobPosting save', err);
      toast.current?.show({ severity: 'error', summary: 'Error', detail: String(err), life: 5000 });
    }
  };

  const isDisabled = !editMode;

  const colsLg = 3;
  const colsMd = 2;
  const colsSm = 1;
  const fullWidthTypes = ["InputTextarea", "QuillEditor", "MonacoEditor", "MarkdownEditor", "FileUpload"];


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
          <Button label="New" icon="pi pi-plus" className="p-button-success p-button-sm" onClick={() => { reset({}); setEditMode(true); if (onNew) onNew(); }} />
        )}
      </div>
      {showForm && (
      <form onSubmit={handleSubmit(onSubmit)}>
      <div className="p-fluid">
      <div className="grid">
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="title">Title</label>
            <Controller name="title" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="title" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('title') ? 'p-invalid' : ''} aria-describedby="title-error" />
              )}
            />
            {getErrorMessage('title') && <small id="title-error" className="p-error">{getErrorMessage('title')}</small>}
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
            <label htmlFor="location">Location</label>
            <Controller name="location" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="location" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('location') ? 'p-invalid' : ''} aria-describedby="location-error" />
              )}
            />
            {getErrorMessage('location') && <small id="location-error" className="p-error">{getErrorMessage('location')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="salarymin">Salarymin</label>
            <Controller name="salarymin" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="salarymin" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('salarymin') ? 'p-invalid' : ''} aria-describedby="salarymin-error" />
              )}
            />
            {getErrorMessage('salarymin') && <small id="salarymin-error" className="p-error">{getErrorMessage('salarymin')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="salarymax">Salarymax</label>
            <Controller name="salarymax" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="salarymax" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('salarymax') ? 'p-invalid' : ''} aria-describedby="salarymax-error" />
              )}
            />
            {getErrorMessage('salarymax') && <small id="salarymax-error" className="p-error">{getErrorMessage('salarymax')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="jobtype">Jobtype</label>
            <Controller name="jobtype" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="jobtype" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('jobtype') ? 'p-invalid' : ''} aria-describedby="jobtype-error" />
              )}
            />
            {getErrorMessage('jobtype') && <small id="jobtype-error" className="p-error">{getErrorMessage('jobtype')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isactive">Isactive</label>
            <Controller name="isactive" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isactive" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isactive') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isactive') && <small id="isactive-error" className="p-error">{getErrorMessage('isactive')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.jobPostingId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
        {canGrantAccess && data?.jobPostingId && (
          <Button label="Grant Access" icon="pi pi-lock-open" className="p-button-warning p-ml-2" type="button" onClick={() => { /* Grant access handler */ }} />
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default JobPostingForm;