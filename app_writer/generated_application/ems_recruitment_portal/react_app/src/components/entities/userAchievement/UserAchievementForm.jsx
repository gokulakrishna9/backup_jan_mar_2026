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
import { createUserAchievement } from '../../../store/slices/userAchievementSlice';
import { updateUserAchievement } from '../../../store/slices/userAchievementSlice';
import logger from '../../../utils/logger';

const UserAchievementForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/userachievements');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      userId: null,
      title: '',
      description: '',
      achievementType: '',
      issuer: '',
      dateAchieved: null,
      url: '',
      documentId: null,
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
      if (data?.achievementId) {
        await dispatch(updateUserAchievement({ id: data.achievementId, data: submitData })).unwrap();
      } else {
        await dispatch(createUserAchievement(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('UserAchievement save', err);
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
            <label htmlFor="title">Title <span className="p-error">*</span></label>
            <Controller name="title" control={control} rules={ {required: 'Title is required',maxLength: { value: 255, message: 'Title cannot exceed 255 characters' },} }
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
            <label htmlFor="achievementType">Achievement Type</label>
            <Controller name="achievementType" control={control} rules={ {maxLength: { value: 100, message: 'Achievementtype cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="achievementType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('achievementType') ? 'p-invalid' : ''} aria-describedby="achievementType-error" />
              )}
            />
            {getErrorMessage('achievementType') && <small id="achievementType-error" className="p-error">{getErrorMessage('achievementType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="issuer">Issuer</label>
            <Controller name="issuer" control={control} rules={ {maxLength: { value: 255, message: 'Issuer cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="issuer" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('issuer') ? 'p-invalid' : ''} aria-describedby="issuer-error" />
              )}
            />
            {getErrorMessage('issuer') && <small id="issuer-error" className="p-error">{getErrorMessage('issuer')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="dateAchieved">Date Achieved</label>
            <Controller name="dateAchieved" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="dateAchieved" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('dateAchieved') ? 'p-invalid' : ''} aria-describedby="dateAchieved-error" />
              )}
            />
            {getErrorMessage('dateAchieved') && <small id="dateAchieved-error" className="p-error">{getErrorMessage('dateAchieved')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="url">Url</label>
            <Controller name="url" control={control} rules={ {maxLength: { value: 500, message: 'Url cannot exceed 500 characters' },} }
              render={({ field: f }) => (
                <InputText id="url" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('url') ? 'p-invalid' : ''} aria-describedby="url-error" />
              )}
            />
            {getErrorMessage('url') && <small id="url-error" className="p-error">{getErrorMessage('url')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="documentId">Document Id</label>
            <Controller name="documentId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="documentId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('documentId') ? 'p-invalid' : ''} aria-describedby="documentId-error" />
              )}
            />
            {getErrorMessage('documentId') && <small id="documentId-error" className="p-error">{getErrorMessage('documentId')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.achievementId && (
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

export default UserAchievementForm;