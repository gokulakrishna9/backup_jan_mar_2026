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
import { createCourseCommunityLink } from '../../../store/slices/courseCommunityLinkSlice';
import { updateCourseCommunityLink } from '../../../store/slices/courseCommunityLinkSlice';
import logger from '../../../utils/logger';

const CourseCommunityLinkForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/coursecommunitylinks');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      courseId: null,
      communityId: null,
      linkType: '',
      isActive: null,
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
      if (data?.linkId) {
        await dispatch(updateCourseCommunityLink({ id: data.linkId, data: submitData })).unwrap();
      } else {
        await dispatch(createCourseCommunityLink(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CourseCommunityLink save', err);
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
            <label htmlFor="courseId">Course Id <span className="p-error">*</span></label>
            <Controller name="courseId" control={control} rules={ {required: 'Courseid is required',} }
              render={({ field: f }) => (
                <InputNumber id="courseId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('courseId') ? 'p-invalid' : ''} aria-describedby="courseId-error" />
              )}
            />
            {getErrorMessage('courseId') && <small id="courseId-error" className="p-error">{getErrorMessage('courseId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="communityId">Community Id <span className="p-error">*</span></label>
            <Controller name="communityId" control={control} rules={ {required: 'Communityid is required',} }
              render={({ field: f }) => (
                <InputNumber id="communityId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('communityId') ? 'p-invalid' : ''} aria-describedby="communityId-error" />
              )}
            />
            {getErrorMessage('communityId') && <small id="communityId-error" className="p-error">{getErrorMessage('communityId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="linkType">Link Type</label>
            <Controller name="linkType" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="linkType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('linkType') ? 'p-invalid' : ''} aria-describedby="linkType-error" />
              )}
            />
            {getErrorMessage('linkType') && <small id="linkType-error" className="p-error">{getErrorMessage('linkType')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isActive">Is Active</label>
            <Controller name="isActive" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isActive" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isActive') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isActive') && <small id="isActive-error" className="p-error">{getErrorMessage('isActive')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.linkId && (
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

export default CourseCommunityLinkForm;