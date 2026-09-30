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
import { createUserEducation } from '../../../store/slices/userEducationSlice';
import { updateUserEducation } from '../../../store/slices/userEducationSlice';
import logger from '../../../utils/logger';

const UserEducationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/user_educations');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      institutionname: '',
      degree: '',
      fieldofstudy: '',
      startdate: null,
      enddate: null,
      grade: '',
      description: '',
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
      if (data?.userEducationId) {
        await dispatch(updateUserEducation({ id: data.userEducationId, data: submitData })).unwrap();
      } else {
        await dispatch(createUserEducation(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('UserEducation save', err);
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
            <label htmlFor="institutionname">Institutionname</label>
            <Controller name="institutionname" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="institutionname" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('institutionname') ? 'p-invalid' : ''} aria-describedby="institutionname-error" />
              )}
            />
            {getErrorMessage('institutionname') && <small id="institutionname-error" className="p-error">{getErrorMessage('institutionname')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="degree">Degree</label>
            <Controller name="degree" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="degree" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('degree') ? 'p-invalid' : ''} aria-describedby="degree-error" />
              )}
            />
            {getErrorMessage('degree') && <small id="degree-error" className="p-error">{getErrorMessage('degree')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="fieldofstudy">Fieldofstudy</label>
            <Controller name="fieldofstudy" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="fieldofstudy" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('fieldofstudy') ? 'p-invalid' : ''} aria-describedby="fieldofstudy-error" />
              )}
            />
            {getErrorMessage('fieldofstudy') && <small id="fieldofstudy-error" className="p-error">{getErrorMessage('fieldofstudy')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="startdate">Startdate</label>
            <Controller name="startdate" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="startdate" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('startdate') ? 'p-invalid' : ''} aria-describedby="startdate-error" />
              )}
            />
            {getErrorMessage('startdate') && <small id="startdate-error" className="p-error">{getErrorMessage('startdate')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="enddate">Enddate</label>
            <Controller name="enddate" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="enddate" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('enddate') ? 'p-invalid' : ''} aria-describedby="enddate-error" />
              )}
            />
            {getErrorMessage('enddate') && <small id="enddate-error" className="p-error">{getErrorMessage('enddate')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="grade">Grade</label>
            <Controller name="grade" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="grade" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('grade') ? 'p-invalid' : ''} aria-describedby="grade-error" />
              )}
            />
            {getErrorMessage('grade') && <small id="grade-error" className="p-error">{getErrorMessage('grade')}</small>}
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
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.userEducationId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
        {canGrantAccess && data?.userEducationId && (
          <Button label="Grant Access" icon="pi pi-lock-open" className="p-button-warning p-ml-2" type="button" onClick={() => { /* Grant access handler */ }} />
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default UserEducationForm;