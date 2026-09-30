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
import { createInstitutionAccreditation } from '../../../store/slices/institutionAccreditationSlice';
import { updateInstitutionAccreditation } from '../../../store/slices/institutionAccreditationSlice';
import logger from '../../../utils/logger';

const InstitutionAccreditationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/institutionaccreditations');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      institutionId: null,
      accreditingBody: '',
      accreditationType: '',
      accreditationLevel: '',
      issueDate: null,
      expiryDate: null,
      certificateDocumentId: null,
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
      if (data?.accreditationId) {
        await dispatch(updateInstitutionAccreditation({ id: data.accreditationId, data: submitData })).unwrap();
      } else {
        await dispatch(createInstitutionAccreditation(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('InstitutionAccreditation save', err);
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
            <label htmlFor="accreditingBody">Accrediting Body <span className="p-error">*</span></label>
            <Controller name="accreditingBody" control={control} rules={ {required: 'Accreditingbody is required',maxLength: { value: 255, message: 'Accreditingbody cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="accreditingBody" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('accreditingBody') ? 'p-invalid' : ''} aria-describedby="accreditingBody-error" />
              )}
            />
            {getErrorMessage('accreditingBody') && <small id="accreditingBody-error" className="p-error">{getErrorMessage('accreditingBody')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="accreditationType">Accreditation Type</label>
            <Controller name="accreditationType" control={control} rules={ {maxLength: { value: 255, message: 'Accreditationtype cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="accreditationType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('accreditationType') ? 'p-invalid' : ''} aria-describedby="accreditationType-error" />
              )}
            />
            {getErrorMessage('accreditationType') && <small id="accreditationType-error" className="p-error">{getErrorMessage('accreditationType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="accreditationLevel">Accreditation Level</label>
            <Controller name="accreditationLevel" control={control} rules={ {maxLength: { value: 100, message: 'Accreditationlevel cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="accreditationLevel" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('accreditationLevel') ? 'p-invalid' : ''} aria-describedby="accreditationLevel-error" />
              )}
            />
            {getErrorMessage('accreditationLevel') && <small id="accreditationLevel-error" className="p-error">{getErrorMessage('accreditationLevel')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="issueDate">Issue Date <span className="p-error">*</span></label>
            <Controller name="issueDate" control={control} rules={ {required: 'Issuedate is required',} }
              render={({ field: f }) => (
                <Calendar id="issueDate" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('issueDate') ? 'p-invalid' : ''} aria-describedby="issueDate-error" />
              )}
            />
            {getErrorMessage('issueDate') && <small id="issueDate-error" className="p-error">{getErrorMessage('issueDate')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="expiryDate">Expiry Date</label>
            <Controller name="expiryDate" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="expiryDate" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('expiryDate') ? 'p-invalid' : ''} aria-describedby="expiryDate-error" />
              )}
            />
            {getErrorMessage('expiryDate') && <small id="expiryDate-error" className="p-error">{getErrorMessage('expiryDate')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="certificateDocumentId">Certificate Document Id</label>
            <Controller name="certificateDocumentId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="certificateDocumentId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('certificateDocumentId') ? 'p-invalid' : ''} aria-describedby="certificateDocumentId-error" />
              )}
            />
            {getErrorMessage('certificateDocumentId') && <small id="certificateDocumentId-error" className="p-error">{getErrorMessage('certificateDocumentId')}</small>}
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
        {!editMode && canUpdate && data?.accreditationId && (
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

export default InstitutionAccreditationForm;