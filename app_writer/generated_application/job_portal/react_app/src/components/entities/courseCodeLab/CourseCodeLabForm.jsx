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
import { createCourseCodeLab } from '../../../store/slices/courseCodeLabSlice';
import { updateCourseCodeLab } from '../../../store/slices/courseCodeLabSlice';
import logger from '../../../utils/logger';

const CourseCodeLabForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true, parentId }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/course_code_labs');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      title: '',
      description: '',
      language: '',
      startercode: '',
      solutioncode: '',
      instructions: '',
      sortorder: null,
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
      if (data?.courseCodeLabId) {
        await dispatch(updateCourseCodeLab({ id: data.courseCodeLabId, data: submitData })).unwrap();
      } else {
        await dispatch(createCourseCodeLab(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CourseCodeLab save', err);
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="language">Language</label>
            <Controller name="language" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="language" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('language') ? 'p-invalid' : ''} aria-describedby="language-error" />
              )}
            />
            {getErrorMessage('language') && <small id="language-error" className="p-error">{getErrorMessage('language')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="startercode">Startercode</label>
            <Controller name="startercode" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="startercode" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('startercode') ? 'p-invalid' : ''} aria-describedby="startercode-error" />
              )}
            />
            {getErrorMessage('startercode') && <small id="startercode-error" className="p-error">{getErrorMessage('startercode')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="solutioncode">Solutioncode</label>
            <Controller name="solutioncode" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="solutioncode" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('solutioncode') ? 'p-invalid' : ''} aria-describedby="solutioncode-error" />
              )}
            />
            {getErrorMessage('solutioncode') && <small id="solutioncode-error" className="p-error">{getErrorMessage('solutioncode')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="instructions">Instructions</label>
            <Controller name="instructions" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="instructions" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('instructions') ? 'p-invalid' : ''} aria-describedby="instructions-error" />
              )}
            />
            {getErrorMessage('instructions') && <small id="instructions-error" className="p-error">{getErrorMessage('instructions')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="sortorder">Sortorder</label>
            <Controller name="sortorder" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="sortorder" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('sortorder') ? 'p-invalid' : ''} aria-describedby="sortorder-error" />
              )}
            />
            {getErrorMessage('sortorder') && <small id="sortorder-error" className="p-error">{getErrorMessage('sortorder')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.courseCodeLabId && (
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

export default CourseCodeLabForm;