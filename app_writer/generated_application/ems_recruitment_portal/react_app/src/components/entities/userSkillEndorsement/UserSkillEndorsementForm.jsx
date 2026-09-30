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
import { createUserSkillEndorsement } from '../../../store/slices/userSkillEndorsementSlice';
import { updateUserSkillEndorsement } from '../../../store/slices/userSkillEndorsementSlice';
import logger from '../../../utils/logger';

const UserSkillEndorsementForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/userskillendorsements');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      skillId: null,
      endorsedByUserId: null,
      endorsementComment: '',
      relationship: '',
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
      if (data?.endorsementId) {
        await dispatch(updateUserSkillEndorsement({ id: data.endorsementId, data: submitData })).unwrap();
      } else {
        await dispatch(createUserSkillEndorsement(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('UserSkillEndorsement save', err);
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
            <label htmlFor="skillId">Skill Id <span className="p-error">*</span></label>
            <Controller name="skillId" control={control} rules={ {required: 'Skillid is required',} }
              render={({ field: f }) => (
                <InputNumber id="skillId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('skillId') ? 'p-invalid' : ''} aria-describedby="skillId-error" />
              )}
            />
            {getErrorMessage('skillId') && <small id="skillId-error" className="p-error">{getErrorMessage('skillId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="endorsedByUserId">Endorsed By User Id <span className="p-error">*</span></label>
            <Controller name="endorsedByUserId" control={control} rules={ {required: 'Endorsedbyuserid is required',} }
              render={({ field: f }) => (
                <InputNumber id="endorsedByUserId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('endorsedByUserId') ? 'p-invalid' : ''} aria-describedby="endorsedByUserId-error" />
              )}
            />
            {getErrorMessage('endorsedByUserId') && <small id="endorsedByUserId-error" className="p-error">{getErrorMessage('endorsedByUserId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="endorsementComment">Endorsement Comment</label>
            <Controller name="endorsementComment" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="endorsementComment" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('endorsementComment') ? 'p-invalid' : ''} aria-describedby="endorsementComment-error" />
              )}
            />
            {getErrorMessage('endorsementComment') && <small id="endorsementComment-error" className="p-error">{getErrorMessage('endorsementComment')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="relationship">Relationship</label>
            <Controller name="relationship" control={control} rules={ {maxLength: { value: 100, message: 'Relationship cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="relationship" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('relationship') ? 'p-invalid' : ''} aria-describedby="relationship-error" />
              )}
            />
            {getErrorMessage('relationship') && <small id="relationship-error" className="p-error">{getErrorMessage('relationship')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.endorsementId && (
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

export default UserSkillEndorsementForm;