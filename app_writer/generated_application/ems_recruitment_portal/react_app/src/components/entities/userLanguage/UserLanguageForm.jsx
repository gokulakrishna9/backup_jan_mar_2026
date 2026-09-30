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
import { createUserLanguage } from '../../../store/slices/userLanguageSlice';
import { updateUserLanguage } from '../../../store/slices/userLanguageSlice';
import logger from '../../../utils/logger';

const UserLanguageForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/userlanguages');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      userId: null,
      languageName: '',
      proficiencyLevel: '',
      canRead: null,
      canWrite: null,
      canSpeak: null,
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
      if (data?.languageId) {
        await dispatch(updateUserLanguage({ id: data.languageId, data: submitData })).unwrap();
      } else {
        await dispatch(createUserLanguage(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('UserLanguage save', err);
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
            <label htmlFor="languageName">Language Name <span className="p-error">*</span></label>
            <Controller name="languageName" control={control} rules={ {required: 'Languagename is required',maxLength: { value: 100, message: 'Languagename cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="languageName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('languageName') ? 'p-invalid' : ''} aria-describedby="languageName-error" />
              )}
            />
            {getErrorMessage('languageName') && <small id="languageName-error" className="p-error">{getErrorMessage('languageName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="proficiencyLevel">Proficiency Level</label>
            <Controller name="proficiencyLevel" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="proficiencyLevel" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('proficiencyLevel') ? 'p-invalid' : ''} aria-describedby="proficiencyLevel-error" />
              )}
            />
            {getErrorMessage('proficiencyLevel') && <small id="proficiencyLevel-error" className="p-error">{getErrorMessage('proficiencyLevel')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="canRead">Can Read</label>
            <Controller name="canRead" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="canRead" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('canRead') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('canRead') && <small id="canRead-error" className="p-error">{getErrorMessage('canRead')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="canWrite">Can Write</label>
            <Controller name="canWrite" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="canWrite" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('canWrite') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('canWrite') && <small id="canWrite-error" className="p-error">{getErrorMessage('canWrite')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="canSpeak">Can Speak</label>
            <Controller name="canSpeak" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="canSpeak" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('canSpeak') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('canSpeak') && <small id="canSpeak-error" className="p-error">{getErrorMessage('canSpeak')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.languageId && (
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

export default UserLanguageForm;