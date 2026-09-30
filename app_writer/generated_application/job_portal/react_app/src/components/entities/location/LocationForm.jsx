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
import { createLocation } from '../../../store/slices/locationSlice';
import { updateLocation } from '../../../store/slices/locationSlice';
import logger from '../../../utils/logger';

const LocationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/locations');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      city: '',
      state: '',
      country: '',
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
      if (data?.locationId) {
        await dispatch(updateLocation({ id: data.locationId, data: submitData })).unwrap();
      } else {
        await dispatch(createLocation(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('Location save', err);
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
            <label htmlFor="city">City</label>
            <Controller name="city" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="city" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('city') ? 'p-invalid' : ''} aria-describedby="city-error" />
              )}
            />
            {getErrorMessage('city') && <small id="city-error" className="p-error">{getErrorMessage('city')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="state">State</label>
            <Controller name="state" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="state" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('state') ? 'p-invalid' : ''} aria-describedby="state-error" />
              )}
            />
            {getErrorMessage('state') && <small id="state-error" className="p-error">{getErrorMessage('state')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="country">Country</label>
            <Controller name="country" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="country" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('country') ? 'p-invalid' : ''} aria-describedby="country-error" />
              )}
            />
            {getErrorMessage('country') && <small id="country-error" className="p-error">{getErrorMessage('country')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.locationId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
        {canGrantAccess && data?.locationId && (
          <Button label="Grant Access" icon="pi pi-lock-open" className="p-button-warning p-ml-2" type="button" onClick={() => { /* Grant access handler */ }} />
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default LocationForm;