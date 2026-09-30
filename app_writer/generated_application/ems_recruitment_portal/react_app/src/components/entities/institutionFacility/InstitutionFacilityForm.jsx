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
import { createInstitutionFacility } from '../../../store/slices/institutionFacilitySlice';
import { updateInstitutionFacility } from '../../../store/slices/institutionFacilitySlice';
import logger from '../../../utils/logger';

const InstitutionFacilityForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/institutionfacilitys');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      institutionId: null,
      facilityName: '',
      facilityType: '',
      description: '',
      capacity: null,
      locationId: null,
      isAvailable: null,
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
      if (data?.facilityId) {
        await dispatch(updateInstitutionFacility({ id: data.facilityId, data: submitData })).unwrap();
      } else {
        await dispatch(createInstitutionFacility(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('InstitutionFacility save', err);
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
            <label htmlFor="facilityName">Facility Name <span className="p-error">*</span></label>
            <Controller name="facilityName" control={control} rules={ {required: 'Facilityname is required',maxLength: { value: 255, message: 'Facilityname cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="facilityName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('facilityName') ? 'p-invalid' : ''} aria-describedby="facilityName-error" />
              )}
            />
            {getErrorMessage('facilityName') && <small id="facilityName-error" className="p-error">{getErrorMessage('facilityName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="facilityType">Facility Type</label>
            <Controller name="facilityType" control={control} rules={ {maxLength: { value: 100, message: 'Facilitytype cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="facilityType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('facilityType') ? 'p-invalid' : ''} aria-describedby="facilityType-error" />
              )}
            />
            {getErrorMessage('facilityType') && <small id="facilityType-error" className="p-error">{getErrorMessage('facilityType')}</small>}
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
            <label htmlFor="capacity">Capacity</label>
            <Controller name="capacity" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="capacity" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('capacity') ? 'p-invalid' : ''} aria-describedby="capacity-error" />
              )}
            />
            {getErrorMessage('capacity') && <small id="capacity-error" className="p-error">{getErrorMessage('capacity')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="locationId">Location Id</label>
            <Controller name="locationId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="locationId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('locationId') ? 'p-invalid' : ''} aria-describedby="locationId-error" />
              )}
            />
            {getErrorMessage('locationId') && <small id="locationId-error" className="p-error">{getErrorMessage('locationId')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isAvailable">Is Available</label>
            <Controller name="isAvailable" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isAvailable" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isAvailable') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isAvailable') && <small id="isAvailable-error" className="p-error">{getErrorMessage('isAvailable')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.facilityId && (
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

export default InstitutionFacilityForm;