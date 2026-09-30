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
import { createPostFlag } from '../../../store/slices/postFlagSlice';
import { updatePostFlag } from '../../../store/slices/postFlagSlice';
import logger from '../../../utils/logger';

const PostFlagForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/postflags');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      type: '',
      userId: null,
      postId: null,
      reason: '',
      flaggedOn: null,
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
      if (data?.flagId) {
        await dispatch(updatePostFlag({ id: data.flagId, data: submitData })).unwrap();
      } else {
        await dispatch(createPostFlag(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('PostFlag save', err);
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="type">Type <span className="p-error">*</span></label>
            <Controller name="type" control={control} rules={ {required: 'Type is required',maxLength: { value: 100, message: 'Type cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="type" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('type') ? 'p-invalid' : ''} aria-describedby="type-error" />
              )}
            />
            {getErrorMessage('type') && <small id="type-error" className="p-error">{getErrorMessage('type')}</small>}
          </div>
        </div>
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
            <label htmlFor="postId">Post Id <span className="p-error">*</span></label>
            <Controller name="postId" control={control} rules={ {required: 'Postid is required',} }
              render={({ field: f }) => (
                <InputNumber id="postId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('postId') ? 'p-invalid' : ''} aria-describedby="postId-error" />
              )}
            />
            {getErrorMessage('postId') && <small id="postId-error" className="p-error">{getErrorMessage('postId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="reason">Reason</label>
            <Controller name="reason" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="reason" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('reason') ? 'p-invalid' : ''} aria-describedby="reason-error" />
              )}
            />
            {getErrorMessage('reason') && <small id="reason-error" className="p-error">{getErrorMessage('reason')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="flaggedOn">Flagged On</label>
            <Controller name="flaggedOn" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="flaggedOn" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('flaggedOn') ? 'p-invalid' : ''} aria-describedby="flaggedOn-error" />
              )}
            />
            {getErrorMessage('flaggedOn') && <small id="flaggedOn-error" className="p-error">{getErrorMessage('flaggedOn')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.flagId && (
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

export default PostFlagForm;