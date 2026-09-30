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

const UserWorkExperienceForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/userworkexperiences');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      userId: null,
      institutionId: null,
      jobTitle: '',
      companyName: '',
      employmentType: '',
      location: '',
      startDate: null,
      endDate: null,
      isCurrent: null,
      responsibilities: '',
      achievements: '',
      skillsUsed: '',
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
      if (data?.experienceId) {
        await dispatch(updateUserWorkExperience({ id: data.experienceId, data: submitData })).unwrap();
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
            <label htmlFor="jobTitle">Job Title <span className="p-error">*</span></label>
            <Controller name="jobTitle" control={control} rules={ {required: 'Jobtitle is required',maxLength: { value: 255, message: 'Jobtitle cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="jobTitle" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('jobTitle') ? 'p-invalid' : ''} aria-describedby="jobTitle-error" />
              )}
            />
            {getErrorMessage('jobTitle') && <small id="jobTitle-error" className="p-error">{getErrorMessage('jobTitle')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="companyName">Company Name <span className="p-error">*</span></label>
            <Controller name="companyName" control={control} rules={ {required: 'Companyname is required',maxLength: { value: 255, message: 'Companyname cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="companyName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('companyName') ? 'p-invalid' : ''} aria-describedby="companyName-error" />
              )}
            />
            {getErrorMessage('companyName') && <small id="companyName-error" className="p-error">{getErrorMessage('companyName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="employmentType">Employment Type</label>
            <Controller name="employmentType" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="employmentType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('employmentType') ? 'p-invalid' : ''} aria-describedby="employmentType-error" />
              )}
            />
            {getErrorMessage('employmentType') && <small id="employmentType-error" className="p-error">{getErrorMessage('employmentType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="location">Location</label>
            <Controller name="location" control={control} rules={ {maxLength: { value: 255, message: 'Location cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="location" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('location') ? 'p-invalid' : ''} aria-describedby="location-error" />
              )}
            />
            {getErrorMessage('location') && <small id="location-error" className="p-error">{getErrorMessage('location')}</small>}
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
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isCurrent">Is Current</label>
            <Controller name="isCurrent" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isCurrent" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isCurrent') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isCurrent') && <small id="isCurrent-error" className="p-error">{getErrorMessage('isCurrent')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="responsibilities">Responsibilities</label>
            <Controller name="responsibilities" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="responsibilities" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('responsibilities') ? 'p-invalid' : ''} aria-describedby="responsibilities-error" />
              )}
            />
            {getErrorMessage('responsibilities') && <small id="responsibilities-error" className="p-error">{getErrorMessage('responsibilities')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="achievements">Achievements</label>
            <Controller name="achievements" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="achievements" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('achievements') ? 'p-invalid' : ''} aria-describedby="achievements-error" />
              )}
            />
            {getErrorMessage('achievements') && <small id="achievements-error" className="p-error">{getErrorMessage('achievements')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="skillsUsed">Skills Used</label>
            <Controller name="skillsUsed" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="skillsUsed" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('skillsUsed') ? 'p-invalid' : ''} aria-describedby="skillsUsed-error" />
              )}
            />
            {getErrorMessage('skillsUsed') && <small id="skillsUsed-error" className="p-error">{getErrorMessage('skillsUsed')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.experienceId && (
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

export default UserWorkExperienceForm;