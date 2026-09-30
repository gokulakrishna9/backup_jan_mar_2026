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
import { createCommunity } from '../../../store/slices/communitySlice';
import { updateCommunity } from '../../../store/slices/communitySlice';
import logger from '../../../utils/logger';

const CommunityForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/communitys');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      instituteId: null,
      name: '',
      description: '',
      groupOwnerUserId: null,
      isEntity: null,
      isPublic: null,
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
      if (data?.communityId) {
        await dispatch(updateCommunity({ id: data.communityId, data: submitData })).unwrap();
      } else {
        await dispatch(createCommunity(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('Community save', err);
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
            <label htmlFor="instituteId">Institute Id</label>
            <Controller name="instituteId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="instituteId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('instituteId') ? 'p-invalid' : ''} aria-describedby="instituteId-error" />
              )}
            />
            {getErrorMessage('instituteId') && <small id="instituteId-error" className="p-error">{getErrorMessage('instituteId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="name">Name <span className="p-error">*</span></label>
            <Controller name="name" control={control} rules={ {required: 'Name is required',maxLength: { value: 255, message: 'Name cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="name" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('name') ? 'p-invalid' : ''} aria-describedby="name-error" />
              )}
            />
            {getErrorMessage('name') && <small id="name-error" className="p-error">{getErrorMessage('name')}</small>}
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
            <label htmlFor="groupOwnerUserId">Group Owner User Id</label>
            <Controller name="groupOwnerUserId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="groupOwnerUserId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('groupOwnerUserId') ? 'p-invalid' : ''} aria-describedby="groupOwnerUserId-error" />
              )}
            />
            {getErrorMessage('groupOwnerUserId') && <small id="groupOwnerUserId-error" className="p-error">{getErrorMessage('groupOwnerUserId')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isEntity">Is Entity</label>
            <Controller name="isEntity" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isEntity" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isEntity') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isEntity') && <small id="isEntity-error" className="p-error">{getErrorMessage('isEntity')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isPublic">Is Public <span className="p-error">*</span></label>
            <Controller name="isPublic" control={control} rules={ {required: 'Ispublic is required',} }
              render={({ field: f }) => (
                <Checkbox id="isPublic" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isPublic') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isPublic') && <small id="isPublic-error" className="p-error">{getErrorMessage('isPublic')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.communityId && (
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

export default CommunityForm;