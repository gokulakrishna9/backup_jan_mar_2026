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
import { createTrainingExam } from '../../../store/slices/trainingExamSlice';
import { updateTrainingExam } from '../../../store/slices/trainingExamSlice';
import logger from '../../../utils/logger';

const TrainingExamForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/training_exams');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      title: '',
      description: '',
      passingscore: null,
      maxscore: null,
      timelimitminutes: null,
      maxattempts: null,
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
      if (data?.trainingExamId) {
        await dispatch(updateTrainingExam({ id: data.trainingExamId, data: submitData })).unwrap();
      } else {
        await dispatch(createTrainingExam(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('TrainingExam save', err);
      toast.current?.show({ severity: 'error', summary: 'Error', detail: String(err), life: 5000 });
    }
  };

  const isDisabled = !editMode;

  const colsLg = 3;
  const colsMd = 2;
  const colsSm = 1;
  const fullWidthTypes = ['InputTextarea', 'QuillEditor', 'MonacoEditor', 'MarkdownEditor', 'FileUpload'];


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
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="passingscore">Passingscore</label>
            <Controller name="passingscore" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="passingscore" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('passingscore') ? 'p-invalid' : ''} aria-describedby="passingscore-error" />
              )}
            />
            {getErrorMessage('passingscore') && <small id="passingscore-error" className="p-error">{getErrorMessage('passingscore')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="maxscore">Maxscore</label>
            <Controller name="maxscore" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="maxscore" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('maxscore') ? 'p-invalid' : ''} aria-describedby="maxscore-error" />
              )}
            />
            {getErrorMessage('maxscore') && <small id="maxscore-error" className="p-error">{getErrorMessage('maxscore')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="timelimitminutes">Timelimitminutes</label>
            <Controller name="timelimitminutes" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="timelimitminutes" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('timelimitminutes') ? 'p-invalid' : ''} aria-describedby="timelimitminutes-error" />
              )}
            />
            {getErrorMessage('timelimitminutes') && <small id="timelimitminutes-error" className="p-error">{getErrorMessage('timelimitminutes')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="maxattempts">Maxattempts</label>
            <Controller name="maxattempts" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="maxattempts" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('maxattempts') ? 'p-invalid' : ''} aria-describedby="maxattempts-error" />
              )}
            />
            {getErrorMessage('maxattempts') && <small id="maxattempts-error" className="p-error">{getErrorMessage('maxattempts')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.trainingExamId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
        {canGrantAccess && data?.trainingExamId && (
          <Button label="Grant Access" icon="pi pi-lock-open" className="p-button-warning p-ml-2" type="button" onClick={() => { /* Grant access handler */ }} />
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default TrainingExamForm;