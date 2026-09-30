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

const UserSkillForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true, parentId }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/user_skills');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      skillname: '',
      proficiencylevel: '',
      yearsofexperience: null,
    },
  });

  useEffect(() => {
    if (data) {
      reset({ ...data });
    }
  }, [data, reset]);

  useEffect(() => {
    setEditMode(mode === 'create' || mode === 'edit');
  }, [mode]);



  const onSubmit = async (formData) => {
    const submitData = { ...formData, userEducationId: parentId };
    try {
      if (data?.userSkillId) {
        await dispatch(updateUserSkill({ id: data.userSkillId, data: submitData })).unwrap();
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
  const fullWidthTypes = ['InputTextarea', 'QuillEditor', 'MonacoEditor', 'MarkdownEditor', 'FileUpload'];


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
          <Button label="New" icon="pi pi-plus" className="p-button-success p-button-sm" onClick={() => { reset({}); setEditMode(true); if (onNew) onNew(); }} />
        )}
      </div>
      {showForm && (
      <form onSubmit={handleSubmit(onSubmit)}>
      <div className="p-fluid">
      <div className="grid">
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="skillname">Skillname</label>
            <Controller name="skillname" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="skillname" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('skillname') ? 'p-invalid' : ''} aria-describedby="skillname-error" />
              )}
            />
            {getErrorMessage('skillname') && <small id="skillname-error" className="p-error">{getErrorMessage('skillname')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="proficiencylevel">Proficiencylevel</label>
            <Controller name="proficiencylevel" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="proficiencylevel" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('proficiencylevel') ? 'p-invalid' : ''} aria-describedby="proficiencylevel-error" />
              )}
            />
            {getErrorMessage('proficiencylevel') && <small id="proficiencylevel-error" className="p-error">{getErrorMessage('proficiencylevel')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="yearsofexperience">Yearsofexperience</label>
            <Controller name="yearsofexperience" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="yearsofexperience" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('yearsofexperience') ? 'p-invalid' : ''} aria-describedby="yearsofexperience-error" />
              )}
            />
            {getErrorMessage('yearsofexperience') && <small id="yearsofexperience-error" className="p-error">{getErrorMessage('yearsofexperience')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.userSkillId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default UserSkillForm;