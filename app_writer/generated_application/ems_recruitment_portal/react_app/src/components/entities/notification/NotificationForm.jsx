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
import { createNotification } from '../../../store/slices/notificationSlice';
import { updateNotification } from '../../../store/slices/notificationSlice';
import logger from '../../../utils/logger';

const NotificationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/notifications');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      userId: null,
      notificationType: '',
      title: '',
      message: '',
      relatedEntityType: '',
      relatedEntityId: null,
      actionUrl: '',
      isRead: null,
      readAt: null,
      priority: '',
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
      if (data?.notificationId) {
        await dispatch(updateNotification({ id: data.notificationId, data: submitData })).unwrap();
      } else {
        await dispatch(createNotification(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('Notification save', err);
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
            <label htmlFor="notificationType">Notification Type <span className="p-error">*</span></label>
            <Controller name="notificationType" control={control} rules={ {required: 'Notificationtype is required',maxLength: { value: 100, message: 'Notificationtype cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="notificationType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('notificationType') ? 'p-invalid' : ''} aria-describedby="notificationType-error" />
              )}
            />
            {getErrorMessage('notificationType') && <small id="notificationType-error" className="p-error">{getErrorMessage('notificationType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="title">Title <span className="p-error">*</span></label>
            <Controller name="title" control={control} rules={ {required: 'Title is required',maxLength: { value: 255, message: 'Title cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="title" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('title') ? 'p-invalid' : ''} aria-describedby="title-error" />
              )}
            />
            {getErrorMessage('title') && <small id="title-error" className="p-error">{getErrorMessage('title')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="message">Message <span className="p-error">*</span></label>
            <Controller name="message" control={control} rules={ {required: 'Message is required',} }
              render={({ field: f }) => (
                <InputText id="message" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('message') ? 'p-invalid' : ''} aria-describedby="message-error" />
              )}
            />
            {getErrorMessage('message') && <small id="message-error" className="p-error">{getErrorMessage('message')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="relatedEntityType">Related Entity Type</label>
            <Controller name="relatedEntityType" control={control} rules={ {maxLength: { value: 100, message: 'Relatedentitytype cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="relatedEntityType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('relatedEntityType') ? 'p-invalid' : ''} aria-describedby="relatedEntityType-error" />
              )}
            />
            {getErrorMessage('relatedEntityType') && <small id="relatedEntityType-error" className="p-error">{getErrorMessage('relatedEntityType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="relatedEntityId">Related Entity Id</label>
            <Controller name="relatedEntityId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="relatedEntityId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('relatedEntityId') ? 'p-invalid' : ''} aria-describedby="relatedEntityId-error" />
              )}
            />
            {getErrorMessage('relatedEntityId') && <small id="relatedEntityId-error" className="p-error">{getErrorMessage('relatedEntityId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="actionUrl">Action Url</label>
            <Controller name="actionUrl" control={control} rules={ {maxLength: { value: 500, message: 'Actionurl cannot exceed 500 characters' },} }
              render={({ field: f }) => (
                <InputText id="actionUrl" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('actionUrl') ? 'p-invalid' : ''} aria-describedby="actionUrl-error" />
              )}
            />
            {getErrorMessage('actionUrl') && <small id="actionUrl-error" className="p-error">{getErrorMessage('actionUrl')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isRead">Is Read</label>
            <Controller name="isRead" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isRead" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isRead') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isRead') && <small id="isRead-error" className="p-error">{getErrorMessage('isRead')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="readAt">Read At</label>
            <Controller name="readAt" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="readAt" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('readAt') ? 'p-invalid' : ''} aria-describedby="readAt-error" />
              )}
            />
            {getErrorMessage('readAt') && <small id="readAt-error" className="p-error">{getErrorMessage('readAt')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="priority">Priority</label>
            <Controller name="priority" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="priority" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('priority') ? 'p-invalid' : ''} aria-describedby="priority-error" />
              )}
            />
            {getErrorMessage('priority') && <small id="priority-error" className="p-error">{getErrorMessage('priority')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.notificationId && (
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

export default NotificationForm;