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
import { createUserSkill } from '../../../store/slices/userSkillSlice';
import { updateUserSkill } from '../../../store/slices/userSkillSlice';
import logger from '../../../utils/logger';

const UserSkillForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/userskills');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      userId: null,
      skillName: '',
      skillCategory: '',
      proficiencyLevel: '',
      yearsOfExperience: null,
      isVerified: null,
      verifiedByInstitutionId: null,
      endorsementCount: null,
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
      if (data?.skillId) {
        await dispatch(updateUserSkill({ id: data.skillId, data: submitData })).unwrap();
      } else {
        await dispatch(createUserSkill(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('UserSkill save', err);
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
            <label htmlFor="skillName">Skill Name <span className="p-error">*</span></label>
            <Controller name="skillName" control={control} rules={ {required: 'Skillname is required',maxLength: { value: 255, message: 'Skillname cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="skillName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('skillName') ? 'p-invalid' : ''} aria-describedby="skillName-error" />
              )}
            />
            {getErrorMessage('skillName') && <small id="skillName-error" className="p-error">{getErrorMessage('skillName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="skillCategory">Skill Category</label>
            <Controller name="skillCategory" control={control} rules={ {maxLength: { value: 100, message: 'Skillcategory cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="skillCategory" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('skillCategory') ? 'p-invalid' : ''} aria-describedby="skillCategory-error" />
              )}
            />
            {getErrorMessage('skillCategory') && <small id="skillCategory-error" className="p-error">{getErrorMessage('skillCategory')}</small>}
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
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="yearsOfExperience">Years Of Experience</label>
            <Controller name="yearsOfExperience" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="yearsOfExperience" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('yearsOfExperience') ? 'p-invalid' : ''} aria-describedby="yearsOfExperience-error" />
              )}
            />
            {getErrorMessage('yearsOfExperience') && <small id="yearsOfExperience-error" className="p-error">{getErrorMessage('yearsOfExperience')}</small>}
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
            <label htmlFor="verifiedByInstitutionId">Verified By Institution Id</label>
            <Controller name="verifiedByInstitutionId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="verifiedByInstitutionId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('verifiedByInstitutionId') ? 'p-invalid' : ''} aria-describedby="verifiedByInstitutionId-error" />
              )}
            />
            {getErrorMessage('verifiedByInstitutionId') && <small id="verifiedByInstitutionId-error" className="p-error">{getErrorMessage('verifiedByInstitutionId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="endorsementCount">Endorsement Count</label>
            <Controller name="endorsementCount" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="endorsementCount" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('endorsementCount') ? 'p-invalid' : ''} aria-describedby="endorsementCount-error" />
              )}
            />
            {getErrorMessage('endorsementCount') && <small id="endorsementCount-error" className="p-error">{getErrorMessage('endorsementCount')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.skillId && (
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

export default UserSkillForm;