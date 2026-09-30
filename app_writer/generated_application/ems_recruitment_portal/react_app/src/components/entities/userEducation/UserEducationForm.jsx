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
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/usereducations');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      userId: null,
      institutionId: null,
      degreeType: '',
      fieldOfStudy: '',
      specialization: '',
      startDate: null,
      endDate: null,
      gradeGpa: '',
      isVerified: null,
      certificateDocumentId: null,
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
      if (data?.educationId) {
        await dispatch(updateUserEducation({ id: data.educationId, data: submitData })).unwrap();
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="degreeType">Degree Type <span className="p-error">*</span></label>
            <Controller name="degreeType" control={control} rules={ {required: 'Degreetype is required',maxLength: { value: 100, message: 'Degreetype cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="degreeType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('degreeType') ? 'p-invalid' : ''} aria-describedby="degreeType-error" />
              )}
            />
            {getErrorMessage('degreeType') && <small id="degreeType-error" className="p-error">{getErrorMessage('degreeType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="fieldOfStudy">Field Of Study <span className="p-error">*</span></label>
            <Controller name="fieldOfStudy" control={control} rules={ {required: 'Fieldofstudy is required',maxLength: { value: 255, message: 'Fieldofstudy cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="fieldOfStudy" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('fieldOfStudy') ? 'p-invalid' : ''} aria-describedby="fieldOfStudy-error" />
              )}
            />
            {getErrorMessage('fieldOfStudy') && <small id="fieldOfStudy-error" className="p-error">{getErrorMessage('fieldOfStudy')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="specialization">Specialization</label>
            <Controller name="specialization" control={control} rules={ {maxLength: { value: 255, message: 'Specialization cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="specialization" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('specialization') ? 'p-invalid' : ''} aria-describedby="specialization-error" />
              )}
            />
            {getErrorMessage('specialization') && <small id="specialization-error" className="p-error">{getErrorMessage('specialization')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="startDate">Start Date <span className="p-error">*</span></label>
            <Controller name="startDate" control={control} rules={ {required: 'Startdate is required',} }
              render={({ field: f }) => (
                <Calendar id="startDate" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('startDate') ? 'p-invalid' : ''} aria-describedby="startDate-error" />
              )}
            />
            {getErrorMessage('startDate') && <small id="startDate-error" className="p-error">{getErrorMessage('startDate')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="endDate">End Date</label>
            <Controller name="endDate" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="endDate" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('endDate') ? 'p-invalid' : ''} aria-describedby="endDate-error" />
              )}
            />
            {getErrorMessage('endDate') && <small id="endDate-error" className="p-error">{getErrorMessage('endDate')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="gradeGpa">Grade Gpa</label>
            <Controller name="gradeGpa" control={control} rules={ {maxLength: { value: 50, message: 'Gradegpa cannot exceed 50 characters' },} }
              render={({ field: f }) => (
                <InputText id="gradeGpa" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('gradeGpa') ? 'p-invalid' : ''} aria-describedby="gradeGpa-error" />
              )}
            />
            {getErrorMessage('gradeGpa') && <small id="gradeGpa-error" className="p-error">{getErrorMessage('gradeGpa')}</small>}
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
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.educationId && (
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

export default UserEducationForm;