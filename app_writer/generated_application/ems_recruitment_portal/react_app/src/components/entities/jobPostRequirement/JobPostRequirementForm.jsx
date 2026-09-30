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
import { createJobPostRequirement } from '../../../store/slices/jobPostRequirementSlice';
import { updateJobPostRequirement } from '../../../store/slices/jobPostRequirementSlice';
import logger from '../../../utils/logger';

const JobPostRequirementForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/jobpostrequirements');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      jobPostId: null,
      requirementType: '',
      requirementDescription: '',
      isMandatory: null,
      minimumYears: null,
      proficiencyLevel: '',
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
      if (data?.requirementId) {
        await dispatch(updateJobPostRequirement({ id: data.requirementId, data: submitData })).unwrap();
      } else {
        await dispatch(createJobPostRequirement(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('JobPostRequirement save', err);
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
            <label htmlFor="jobPostId">Job Post Id <span className="p-error">*</span></label>
            <Controller name="jobPostId" control={control} rules={ {required: 'Jobpostid is required',} }
              render={({ field: f }) => (
                <InputNumber id="jobPostId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('jobPostId') ? 'p-invalid' : ''} aria-describedby="jobPostId-error" />
              )}
            />
            {getErrorMessage('jobPostId') && <small id="jobPostId-error" className="p-error">{getErrorMessage('jobPostId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="requirementType">Requirement Type <span className="p-error">*</span></label>
            <Controller name="requirementType" control={control} rules={ {required: 'Requirementtype is required',} }
              render={({ field: f }) => (
                <InputText id="requirementType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('requirementType') ? 'p-invalid' : ''} aria-describedby="requirementType-error" />
              )}
            />
            {getErrorMessage('requirementType') && <small id="requirementType-error" className="p-error">{getErrorMessage('requirementType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="requirementDescription">Requirement Description <span className="p-error">*</span></label>
            <Controller name="requirementDescription" control={control} rules={ {required: 'Requirementdescription is required',} }
              render={({ field: f }) => (
                <InputText id="requirementDescription" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('requirementDescription') ? 'p-invalid' : ''} aria-describedby="requirementDescription-error" />
              )}
            />
            {getErrorMessage('requirementDescription') && <small id="requirementDescription-error" className="p-error">{getErrorMessage('requirementDescription')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isMandatory">Is Mandatory</label>
            <Controller name="isMandatory" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isMandatory" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isMandatory') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isMandatory') && <small id="isMandatory-error" className="p-error">{getErrorMessage('isMandatory')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="minimumYears">Minimum Years</label>
            <Controller name="minimumYears" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="minimumYears" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('minimumYears') ? 'p-invalid' : ''} aria-describedby="minimumYears-error" />
              )}
            />
            {getErrorMessage('minimumYears') && <small id="minimumYears-error" className="p-error">{getErrorMessage('minimumYears')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="proficiencyLevel">Proficiency Level</label>
            <Controller name="proficiencyLevel" control={control} rules={ {maxLength: { value: 100, message: 'Proficiencylevel cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="proficiencyLevel" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('proficiencyLevel') ? 'p-invalid' : ''} aria-describedby="proficiencyLevel-error" />
              )}
            />
            {getErrorMessage('proficiencyLevel') && <small id="proficiencyLevel-error" className="p-error">{getErrorMessage('proficiencyLevel')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.requirementId && (
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

export default JobPostRequirementForm;