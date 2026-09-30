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
import { createTrainingEnrollment } from '../../../store/slices/trainingEnrollmentSlice';
import { updateTrainingEnrollment } from '../../../store/slices/trainingEnrollmentSlice';
import logger from '../../../utils/logger';

const TrainingEnrollmentForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/training_enrollments');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      status: '',
      progress: null,
      enrolledat: null,
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
      if (data?.trainingEnrollmentId) {
        await dispatch(updateTrainingEnrollment({ id: data.trainingEnrollmentId, data: submitData })).unwrap();
      } else {
        await dispatch(createTrainingEnrollment(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('TrainingEnrollment save', err);
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
            <label htmlFor="status">Status</label>
            <Controller name="status" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="status" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('status') ? 'p-invalid' : ''} aria-describedby="status-error" />
              )}
            />
            {getErrorMessage('status') && <small id="status-error" className="p-error">{getErrorMessage('status')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="progress">Progress</label>
            <Controller name="progress" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="progress" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('progress') ? 'p-invalid' : ''} aria-describedby="progress-error" />
              )}
            />
            {getErrorMessage('progress') && <small id="progress-error" className="p-error">{getErrorMessage('progress')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="enrolledat">Enrolledat</label>
            <Controller name="enrolledat" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="enrolledat" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('enrolledat') ? 'p-invalid' : ''} aria-describedby="enrolledat-error" />
              )}
            />
            {getErrorMessage('enrolledat') && <small id="enrolledat-error" className="p-error">{getErrorMessage('enrolledat')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.trainingEnrollmentId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
        {canGrantAccess && data?.trainingEnrollmentId && (
          <Button label="Grant Access" icon="pi pi-lock-open" className="p-button-warning p-ml-2" type="button" onClick={() => { /* Grant access handler */ }} />
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default TrainingEnrollmentForm;