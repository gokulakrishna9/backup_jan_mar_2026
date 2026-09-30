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
import { createTrainingCertification } from '../../../store/slices/trainingCertificationSlice';
import { updateTrainingCertification } from '../../../store/slices/trainingCertificationSlice';
import logger from '../../../utils/logger';

const TrainingCertificationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/training_certifications');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      certificatenumber: '',
      title: '',
      issuedat: null,
      expiresat: null,
      certificateurl: '',
      status: '',
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
      if (data?.trainingCertificationId) {
        await dispatch(updateTrainingCertification({ id: data.trainingCertificationId, data: submitData })).unwrap();
      } else {
        await dispatch(createTrainingCertification(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('TrainingCertification save', err);
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
            <label htmlFor="certificatenumber">Certificatenumber</label>
            <Controller name="certificatenumber" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="certificatenumber" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('certificatenumber') ? 'p-invalid' : ''} aria-describedby="certificatenumber-error" />
              )}
            />
            {getErrorMessage('certificatenumber') && <small id="certificatenumber-error" className="p-error">{getErrorMessage('certificatenumber')}</small>}
          </div>
        </div>
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
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="issuedat">Issuedat</label>
            <Controller name="issuedat" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="issuedat" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('issuedat') ? 'p-invalid' : ''} aria-describedby="issuedat-error" />
              )}
            />
            {getErrorMessage('issuedat') && <small id="issuedat-error" className="p-error">{getErrorMessage('issuedat')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="expiresat">Expiresat</label>
            <Controller name="expiresat" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="expiresat" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('expiresat') ? 'p-invalid' : ''} aria-describedby="expiresat-error" />
              )}
            />
            {getErrorMessage('expiresat') && <small id="expiresat-error" className="p-error">{getErrorMessage('expiresat')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="certificateurl">Certificateurl</label>
            <Controller name="certificateurl" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="certificateurl" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('certificateurl') ? 'p-invalid' : ''} aria-describedby="certificateurl-error" />
              )}
            />
            {getErrorMessage('certificateurl') && <small id="certificateurl-error" className="p-error">{getErrorMessage('certificateurl')}</small>}
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
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.trainingCertificationId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
        {canGrantAccess && data?.trainingCertificationId && (
          <Button label="Grant Access" icon="pi pi-lock-open" className="p-button-warning p-ml-2" type="button" onClick={() => { /* Grant access handler */ }} />
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default TrainingCertificationForm;