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
import { createJobPostFile } from '../../../store/slices/jobPostFileSlice';
import { updateJobPostFile } from '../../../store/slices/jobPostFileSlice';
import logger from '../../../utils/logger';

const JobPostFileForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/jobpostfiles');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      jobPostId: null,
      applicationId: null,
      fileName: '',
      originalFileName: '',
      fileType: '',
      fileExtension: '',
      fileLocation: '',
      fileSizeBytes: null,
      mimeType: '',
      description: '',
      comment: '',
      category: '',
      uploadedByUserId: null,
      downloadCount: null,
      thumbnailLocation: '',
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
      if (data?.fileId) {
        await dispatch(updateJobPostFile({ id: data.fileId, data: submitData })).unwrap();
      } else {
        await dispatch(createJobPostFile(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('JobPostFile save', err);
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
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="applicationId">Application Id</label>
            <Controller name="applicationId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="applicationId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('applicationId') ? 'p-invalid' : ''} aria-describedby="applicationId-error" />
              )}
            />
            {getErrorMessage('applicationId') && <small id="applicationId-error" className="p-error">{getErrorMessage('applicationId')}</small>}
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
            <label htmlFor="originalFileName">Original File Name <span className="p-error">*</span></label>
            <Controller name="originalFileName" control={control} rules={ {required: 'Originalfilename is required',maxLength: { value: 255, message: 'Originalfilename cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="originalFileName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('originalFileName') ? 'p-invalid' : ''} aria-describedby="originalFileName-error" />
              )}
            />
            {getErrorMessage('originalFileName') && <small id="originalFileName-error" className="p-error">{getErrorMessage('originalFileName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="fileType">File Type <span className="p-error">*</span></label>
            <Controller name="fileType" control={control} rules={ {required: 'Filetype is required',} }
              render={({ field: f }) => (
                <InputText id="fileType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('fileType') ? 'p-invalid' : ''} aria-describedby="fileType-error" />
              )}
            />
            {getErrorMessage('fileType') && <small id="fileType-error" className="p-error">{getErrorMessage('fileType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="fileExtension">File Extension</label>
            <Controller name="fileExtension" control={control} rules={ {maxLength: { value: 20, message: 'Fileextension cannot exceed 20 characters' },} }
              render={({ field: f }) => (
                <InputText id="fileExtension" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('fileExtension') ? 'p-invalid' : ''} aria-describedby="fileExtension-error" />
              )}
            />
            {getErrorMessage('fileExtension') && <small id="fileExtension-error" className="p-error">{getErrorMessage('fileExtension')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="fileLocation">File Location <span className="p-error">*</span></label>
            <Controller name="fileLocation" control={control} rules={ {required: 'Filelocation is required',maxLength: { value: 500, message: 'Filelocation cannot exceed 500 characters' },} }
              render={({ field: f }) => (
                <InputText id="fileLocation" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('fileLocation') ? 'p-invalid' : ''} aria-describedby="fileLocation-error" />
              )}
            />
            {getErrorMessage('fileLocation') && <small id="fileLocation-error" className="p-error">{getErrorMessage('fileLocation')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="fileSizeBytes">File Size Bytes</label>
            <Controller name="fileSizeBytes" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="fileSizeBytes" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('fileSizeBytes') ? 'p-invalid' : ''} aria-describedby="fileSizeBytes-error" />
              )}
            />
            {getErrorMessage('fileSizeBytes') && <small id="fileSizeBytes-error" className="p-error">{getErrorMessage('fileSizeBytes')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="mimeType">Mime Type</label>
            <Controller name="mimeType" control={control} rules={ {maxLength: { value: 100, message: 'Mimetype cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="mimeType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('mimeType') ? 'p-invalid' : ''} aria-describedby="mimeType-error" />
              )}
            />
            {getErrorMessage('mimeType') && <small id="mimeType-error" className="p-error">{getErrorMessage('mimeType')}</small>}
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="comment">Comment</label>
            <Controller name="comment" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="comment" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('comment') ? 'p-invalid' : ''} aria-describedby="comment-error" />
              )}
            />
            {getErrorMessage('comment') && <small id="comment-error" className="p-error">{getErrorMessage('comment')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="category">Category</label>
            <Controller name="category" control={control} rules={ {maxLength: { value: 100, message: 'Category cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="category" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('category') ? 'p-invalid' : ''} aria-describedby="category-error" />
              )}
            />
            {getErrorMessage('category') && <small id="category-error" className="p-error">{getErrorMessage('category')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="uploadedByUserId">Uploaded By User Id</label>
            <Controller name="uploadedByUserId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="uploadedByUserId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('uploadedByUserId') ? 'p-invalid' : ''} aria-describedby="uploadedByUserId-error" />
              )}
            />
            {getErrorMessage('uploadedByUserId') && <small id="uploadedByUserId-error" className="p-error">{getErrorMessage('uploadedByUserId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="downloadCount">Download Count</label>
            <Controller name="downloadCount" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="downloadCount" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('downloadCount') ? 'p-invalid' : ''} aria-describedby="downloadCount-error" />
              )}
            />
            {getErrorMessage('downloadCount') && <small id="downloadCount-error" className="p-error">{getErrorMessage('downloadCount')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="thumbnailLocation">Thumbnail Location</label>
            <Controller name="thumbnailLocation" control={control} rules={ {maxLength: { value: 500, message: 'Thumbnaillocation cannot exceed 500 characters' },} }
              render={({ field: f }) => (
                <InputText id="thumbnailLocation" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('thumbnailLocation') ? 'p-invalid' : ''} aria-describedby="thumbnailLocation-error" />
              )}
            />
            {getErrorMessage('thumbnailLocation') && <small id="thumbnailLocation-error" className="p-error">{getErrorMessage('thumbnailLocation')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.fileId && (
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

export default JobPostFileForm;