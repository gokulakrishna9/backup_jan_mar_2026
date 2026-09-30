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
import { createUserCertification } from '../../../store/slices/userCertificationSlice';
import { updateUserCertification } from '../../../store/slices/userCertificationSlice';
import logger from '../../../utils/logger';

const UserCertificationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/usercertifications');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      userId: null,
      certificationName: '',
      issuingOrganization: '',
      institutionId: null,
      issueDate: null,
      expiryDate: null,
      credentialId: '',
      credentialUrl: '',
      certificateDocumentId: null,
      isVerified: null,
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
      if (data?.certificationId) {
        await dispatch(updateUserCertification({ id: data.certificationId, data: submitData })).unwrap();
      } else {
        await dispatch(createUserCertification(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('UserCertification save', err);
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
            <label htmlFor="certificationName">Certification Name <span className="p-error">*</span></label>
            <Controller name="certificationName" control={control} rules={ {required: 'Certificationname is required',maxLength: { value: 255, message: 'Certificationname cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="certificationName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('certificationName') ? 'p-invalid' : ''} aria-describedby="certificationName-error" />
              )}
            />
            {getErrorMessage('certificationName') && <small id="certificationName-error" className="p-error">{getErrorMessage('certificationName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="issuingOrganization">Issuing Organization <span className="p-error">*</span></label>
            <Controller name="issuingOrganization" control={control} rules={ {required: 'Issuingorganization is required',maxLength: { value: 255, message: 'Issuingorganization cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="issuingOrganization" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('issuingOrganization') ? 'p-invalid' : ''} aria-describedby="issuingOrganization-error" />
              )}
            />
            {getErrorMessage('issuingOrganization') && <small id="issuingOrganization-error" className="p-error">{getErrorMessage('issuingOrganization')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="institutionId">Institution Id</label>
            <Controller name="institutionId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="institutionId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('institutionId') ? 'p-invalid' : ''} aria-describedby="institutionId-error" />
              )}
            />
            {getErrorMessage('institutionId') && <small id="institutionId-error" className="p-error">{getErrorMessage('institutionId')}</small>}
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="credentialId">Credential Id</label>
            <Controller name="credentialId" control={control} rules={ {maxLength: { value: 255, message: 'Credentialid cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="credentialId" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('credentialId') ? 'p-invalid' : ''} aria-describedby="credentialId-error" />
              )}
            />
            {getErrorMessage('credentialId') && <small id="credentialId-error" className="p-error">{getErrorMessage('credentialId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="credentialUrl">Credential Url</label>
            <Controller name="credentialUrl" control={control} rules={ {maxLength: { value: 500, message: 'Credentialurl cannot exceed 500 characters' },} }
              render={({ field: f }) => (
                <InputText id="credentialUrl" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('credentialUrl') ? 'p-invalid' : ''} aria-describedby="credentialUrl-error" />
              )}
            />
            {getErrorMessage('credentialUrl') && <small id="credentialUrl-error" className="p-error">{getErrorMessage('credentialUrl')}</small>}
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
            <label htmlFor="isVerified">Is Verified</label>
            <Controller name="isVerified" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isVerified" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isVerified') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isVerified') && <small id="isVerified-error" className="p-error">{getErrorMessage('isVerified')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.certificationId && (
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

export default UserCertificationForm;