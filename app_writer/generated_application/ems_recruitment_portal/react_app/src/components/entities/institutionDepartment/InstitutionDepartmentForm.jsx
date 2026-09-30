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
import { createInstitutionDepartment } from '../../../store/slices/institutionDepartmentSlice';
import { updateInstitutionDepartment } from '../../../store/slices/institutionDepartmentSlice';
import logger from '../../../utils/logger';

const InstitutionDepartmentForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/institutiondepartments');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      institutionId: null,
      departmentName: '',
      description: '',
      headOfDepartmentUserId: null,
      contactEmail: '',
      contactPhone: '',
      isActive: null,
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
      if (data?.departmentId) {
        await dispatch(updateInstitutionDepartment({ id: data.departmentId, data: submitData })).unwrap();
      } else {
        await dispatch(createInstitutionDepartment(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('InstitutionDepartment save', err);
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
            <label htmlFor="departmentName">Department Name <span className="p-error">*</span></label>
            <Controller name="departmentName" control={control} rules={ {required: 'Departmentname is required',maxLength: { value: 255, message: 'Departmentname cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="departmentName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('departmentName') ? 'p-invalid' : ''} aria-describedby="departmentName-error" />
              )}
            />
            {getErrorMessage('departmentName') && <small id="departmentName-error" className="p-error">{getErrorMessage('departmentName')}</small>}
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
            <label htmlFor="headOfDepartmentUserId">Head Of Department User Id</label>
            <Controller name="headOfDepartmentUserId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="headOfDepartmentUserId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('headOfDepartmentUserId') ? 'p-invalid' : ''} aria-describedby="headOfDepartmentUserId-error" />
              )}
            />
            {getErrorMessage('headOfDepartmentUserId') && <small id="headOfDepartmentUserId-error" className="p-error">{getErrorMessage('headOfDepartmentUserId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="contactEmail">Contact Email</label>
            <Controller name="contactEmail" control={control} rules={ {maxLength: { value: 255, message: 'Contactemail cannot exceed 255 characters' },pattern: { value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: 'Please provide a valid email address' },} }
              render={({ field: f }) => (
                <InputText id="contactEmail" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('contactEmail') ? 'p-invalid' : ''} aria-describedby="contactEmail-error" />
              )}
            />
            {getErrorMessage('contactEmail') && <small id="contactEmail-error" className="p-error">{getErrorMessage('contactEmail')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="contactPhone">Contact Phone</label>
            <Controller name="contactPhone" control={control} rules={ {maxLength: { value: 30, message: 'Contactphone cannot exceed 30 characters' },} }
              render={({ field: f }) => (
                <InputText id="contactPhone" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('contactPhone') ? 'p-invalid' : ''} aria-describedby="contactPhone-error" />
              )}
            />
            {getErrorMessage('contactPhone') && <small id="contactPhone-error" className="p-error">{getErrorMessage('contactPhone')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isActive">Is Active</label>
            <Controller name="isActive" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isActive" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isActive') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isActive') && <small id="isActive-error" className="p-error">{getErrorMessage('isActive')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.departmentId && (
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

export default InstitutionDepartmentForm;