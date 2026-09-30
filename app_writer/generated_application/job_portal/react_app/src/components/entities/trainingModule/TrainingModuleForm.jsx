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
import { createTrainingModule } from '../../../store/slices/trainingModuleSlice';
import { updateTrainingModule } from '../../../store/slices/trainingModuleSlice';
import logger from '../../../utils/logger';

const TrainingModuleForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true, parentId }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/training_modules');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      title: '',
      description: '',
      moduleorder: null,
      durationminutes: null,
      contenturl: '',
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
    const submitData = { ...formData, trainingProgramId: parentId };
    try {
      if (data?.trainingModuleId) {
        await dispatch(updateTrainingModule({ id: data.trainingModuleId, data: submitData })).unwrap();
      } else {
        await dispatch(createTrainingModule(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('TrainingModule save', err);
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
            <label htmlFor="moduleorder">Moduleorder</label>
            <Controller name="moduleorder" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="moduleorder" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('moduleorder') ? 'p-invalid' : ''} aria-describedby="moduleorder-error" />
              )}
            />
            {getErrorMessage('moduleorder') && <small id="moduleorder-error" className="p-error">{getErrorMessage('moduleorder')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="durationminutes">Durationminutes</label>
            <Controller name="durationminutes" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="durationminutes" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('durationminutes') ? 'p-invalid' : ''} aria-describedby="durationminutes-error" />
              )}
            />
            {getErrorMessage('durationminutes') && <small id="durationminutes-error" className="p-error">{getErrorMessage('durationminutes')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="contenturl">Contenturl</label>
            <Controller name="contenturl" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="contenturl" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('contenturl') ? 'p-invalid' : ''} aria-describedby="contenturl-error" />
              )}
            />
            {getErrorMessage('contenturl') && <small id="contenturl-error" className="p-error">{getErrorMessage('contenturl')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.trainingModuleId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default TrainingModuleForm;