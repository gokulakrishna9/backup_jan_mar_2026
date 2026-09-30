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
import { createPostAttachment } from '../../../store/slices/postAttachmentSlice';
import { updatePostAttachment } from '../../../store/slices/postAttachmentSlice';
import logger from '../../../utils/logger';

const PostAttachmentForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/postattachments');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      postId: null,
      fileName: '',
      fileType: '',
      fileUrl: '',
      fileSizeKb: null,
      thumbnailUrl: '',
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
      if (data?.attachmentId) {
        await dispatch(updatePostAttachment({ id: data.attachmentId, data: submitData })).unwrap();
      } else {
        await dispatch(createPostAttachment(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('PostAttachment save', err);
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
            <label htmlFor="fileName">File Name <span className="p-error">*</span></label>
            <Controller name="fileName" control={control} rules={ {required: 'Filename is required',maxLength: { value: 255, message: 'Filename cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="fileName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('fileName') ? 'p-invalid' : ''} aria-describedby="fileName-error" />
              )}
            />
            {getErrorMessage('fileName') && <small id="fileName-error" className="p-error">{getErrorMessage('fileName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="fileType">File Type</label>
            <Controller name="fileType" control={control} rules={ {maxLength: { value: 100, message: 'Filetype cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="fileType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('fileType') ? 'p-invalid' : ''} aria-describedby="fileType-error" />
              )}
            />
            {getErrorMessage('fileType') && <small id="fileType-error" className="p-error">{getErrorMessage('fileType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="fileUrl">File Url <span className="p-error">*</span></label>
            <Controller name="fileUrl" control={control} rules={ {required: 'Fileurl is required',maxLength: { value: 500, message: 'Fileurl cannot exceed 500 characters' },} }
              render={({ field: f }) => (
                <InputText id="fileUrl" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('fileUrl') ? 'p-invalid' : ''} aria-describedby="fileUrl-error" />
              )}
            />
            {getErrorMessage('fileUrl') && <small id="fileUrl-error" className="p-error">{getErrorMessage('fileUrl')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="fileSizeKb">File Size Kb</label>
            <Controller name="fileSizeKb" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="fileSizeKb" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('fileSizeKb') ? 'p-invalid' : ''} aria-describedby="fileSizeKb-error" />
              )}
            />
            {getErrorMessage('fileSizeKb') && <small id="fileSizeKb-error" className="p-error">{getErrorMessage('fileSizeKb')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="thumbnailUrl">Thumbnail Url</label>
            <Controller name="thumbnailUrl" control={control} rules={ {maxLength: { value: 500, message: 'Thumbnailurl cannot exceed 500 characters' },} }
              render={({ field: f }) => (
                <InputText id="thumbnailUrl" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('thumbnailUrl') ? 'p-invalid' : ''} aria-describedby="thumbnailUrl-error" />
              )}
            />
            {getErrorMessage('thumbnailUrl') && <small id="thumbnailUrl-error" className="p-error">{getErrorMessage('thumbnailUrl')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.attachmentId && (
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

export default PostAttachmentForm;