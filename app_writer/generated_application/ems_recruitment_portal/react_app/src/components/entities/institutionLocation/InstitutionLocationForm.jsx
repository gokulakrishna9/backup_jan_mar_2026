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
import { createInstitutionLocation } from '../../../store/slices/institutionLocationSlice';
import { updateInstitutionLocation } from '../../../store/slices/institutionLocationSlice';
import logger from '../../../utils/logger';

const InstitutionLocationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/institutionlocations');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      institutionId: null,
      locationType: '',
      addressLine1: '',
      addressLine2: '',
      city: '',
      stateProvince: '',
      country: '',
      postalCode: '',
      latitude: null,
      longitude: null,
      isPrimary: null,
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
      if (data?.locationId) {
        await dispatch(updateInstitutionLocation({ id: data.locationId, data: submitData })).unwrap();
      } else {
        await dispatch(createInstitutionLocation(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('InstitutionLocation save', err);
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
            <label htmlFor="institutionId">Institution Id <span className="p-error">*</span></label>
            <Controller name="institutionId" control={control} rules={ {required: 'Institutionid is required',} }
              render={({ field: f }) => (
                <InputNumber id="institutionId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('institutionId') ? 'p-invalid' : ''} aria-describedby="institutionId-error" />
              )}
            />
            {getErrorMessage('institutionId') && <small id="institutionId-error" className="p-error">{getErrorMessage('institutionId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="locationType">Location Type</label>
            <Controller name="locationType" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="locationType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('locationType') ? 'p-invalid' : ''} aria-describedby="locationType-error" />
              )}
            />
            {getErrorMessage('locationType') && <small id="locationType-error" className="p-error">{getErrorMessage('locationType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="addressLine1">Address Line1 <span className="p-error">*</span></label>
            <Controller name="addressLine1" control={control} rules={ {required: 'Addressline1 is required',maxLength: { value: 255, message: 'Addressline1 cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="addressLine1" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('addressLine1') ? 'p-invalid' : ''} aria-describedby="addressLine1-error" />
              )}
            />
            {getErrorMessage('addressLine1') && <small id="addressLine1-error" className="p-error">{getErrorMessage('addressLine1')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="addressLine2">Address Line2</label>
            <Controller name="addressLine2" control={control} rules={ {maxLength: { value: 255, message: 'Addressline2 cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="addressLine2" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('addressLine2') ? 'p-invalid' : ''} aria-describedby="addressLine2-error" />
              )}
            />
            {getErrorMessage('addressLine2') && <small id="addressLine2-error" className="p-error">{getErrorMessage('addressLine2')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="city">City <span className="p-error">*</span></label>
            <Controller name="city" control={control} rules={ {required: 'City is required',maxLength: { value: 100, message: 'City cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="city" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('city') ? 'p-invalid' : ''} aria-describedby="city-error" />
              )}
            />
            {getErrorMessage('city') && <small id="city-error" className="p-error">{getErrorMessage('city')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="stateProvince">State Province</label>
            <Controller name="stateProvince" control={control} rules={ {maxLength: { value: 100, message: 'Stateprovince cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="stateProvince" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('stateProvince') ? 'p-invalid' : ''} aria-describedby="stateProvince-error" />
              )}
            />
            {getErrorMessage('stateProvince') && <small id="stateProvince-error" className="p-error">{getErrorMessage('stateProvince')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="country">Country <span className="p-error">*</span></label>
            <Controller name="country" control={control} rules={ {required: 'Country is required',maxLength: { value: 100, message: 'Country cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="country" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('country') ? 'p-invalid' : ''} aria-describedby="country-error" />
              )}
            />
            {getErrorMessage('country') && <small id="country-error" className="p-error">{getErrorMessage('country')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="postalCode">Postal Code</label>
            <Controller name="postalCode" control={control} rules={ {maxLength: { value: 20, message: 'Postalcode cannot exceed 20 characters' },} }
              render={({ field: f }) => (
                <InputText id="postalCode" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('postalCode') ? 'p-invalid' : ''} aria-describedby="postalCode-error" />
              )}
            />
            {getErrorMessage('postalCode') && <small id="postalCode-error" className="p-error">{getErrorMessage('postalCode')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="latitude">Latitude</label>
            <Controller name="latitude" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="latitude" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('latitude') ? 'p-invalid' : ''} aria-describedby="latitude-error" />
              )}
            />
            {getErrorMessage('latitude') && <small id="latitude-error" className="p-error">{getErrorMessage('latitude')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="longitude">Longitude</label>
            <Controller name="longitude" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="longitude" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('longitude') ? 'p-invalid' : ''} aria-describedby="longitude-error" />
              )}
            />
            {getErrorMessage('longitude') && <small id="longitude-error" className="p-error">{getErrorMessage('longitude')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isPrimary">Is Primary</label>
            <Controller name="isPrimary" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isPrimary" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isPrimary') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isPrimary') && <small id="isPrimary-error" className="p-error">{getErrorMessage('isPrimary')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.locationId && (
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

export default InstitutionLocationForm;