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
import { createUserWorkExperience } from '../../../store/slices/userWorkExperienceSlice';
import { updateUserWorkExperience } from '../../../store/slices/userWorkExperienceSlice';
import logger from '../../../utils/logger';

const UserWorkExperienceForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true, parentId }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/user_work_experiences');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      companyname: '',
      jobtitle: '',
      industry: '',
      location: '',
      startdate: null,
      enddate: null,
      iscurrent: null,
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
    const submitData = { ...formData, userEducationId: parentId };
    try {
      if (data?.userWorkExperienceId) {
        await dispatch(updateUserWorkExperience({ id: data.userWorkExperienceId, data: submitData })).unwrap();
      } else {
        await dispatch(createUserWorkExperience(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('UserWorkExperience save', err);
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
            <label htmlFor="companyname">Companyname</label>
            <Controller name="companyname" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="companyname" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('companyname') ? 'p-invalid' : ''} aria-describedby="companyname-error" />
              )}
            />
            {getErrorMessage('companyname') && <small id="companyname-error" className="p-error">{getErrorMessage('companyname')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="jobtitle">Jobtitle</label>
            <Controller name="jobtitle" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="jobtitle" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('jobtitle') ? 'p-invalid' : ''} aria-describedby="jobtitle-error" />
              )}
            />
            {getErrorMessage('jobtitle') && <small id="jobtitle-error" className="p-error">{getErrorMessage('jobtitle')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="industry">Industry</label>
            <Controller name="industry" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="industry" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('industry') ? 'p-invalid' : ''} aria-describedby="industry-error" />
              )}
            />
            {getErrorMessage('industry') && <small id="industry-error" className="p-error">{getErrorMessage('industry')}</small>}
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
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="iscurrent">Iscurrent</label>
            <Controller name="iscurrent" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="iscurrent" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('iscurrent') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('iscurrent') && <small id="iscurrent-error" className="p-error">{getErrorMessage('iscurrent')}</small>}
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
        {!editMode && canUpdate && data?.userWorkExperienceId && (
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

export default UserWorkExperienceForm;