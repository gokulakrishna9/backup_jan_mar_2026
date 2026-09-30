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
import { createCourseProperty } from '../../../store/slices/coursePropertySlice';
import { updateCourseProperty } from '../../../store/slices/coursePropertySlice';
import logger from '../../../utils/logger';

const CoursePropertyForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/coursepropertys');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      propertyName: '',
      propertyValue: '',
      propertyType: '',
      propertyDescription: '',
      groupId: null,
      courseId: null,
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
      if (data?.propertyId) {
        await dispatch(updateCourseProperty({ id: data.propertyId, data: submitData })).unwrap();
      } else {
        await dispatch(createCourseProperty(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CourseProperty save', err);
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
            <label htmlFor="propertyName">Property Name <span className="p-error">*</span></label>
            <Controller name="propertyName" control={control} rules={ {required: 'Propertyname is required',maxLength: { value: 150, message: 'Propertyname cannot exceed 150 characters' },} }
              render={({ field: f }) => (
                <InputText id="propertyName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('propertyName') ? 'p-invalid' : ''} aria-describedby="propertyName-error" />
              )}
            />
            {getErrorMessage('propertyName') && <small id="propertyName-error" className="p-error">{getErrorMessage('propertyName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="propertyValue">Property Value</label>
            <Controller name="propertyValue" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="propertyValue" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('propertyValue') ? 'p-invalid' : ''} aria-describedby="propertyValue-error" />
              )}
            />
            {getErrorMessage('propertyValue') && <small id="propertyValue-error" className="p-error">{getErrorMessage('propertyValue')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="propertyType">Property Type <span className="p-error">*</span></label>
            <Controller name="propertyType" control={control} rules={ {required: 'Propertytype is required',maxLength: { value: 50, message: 'Propertytype cannot exceed 50 characters' },} }
              render={({ field: f }) => (
                <InputText id="propertyType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('propertyType') ? 'p-invalid' : ''} aria-describedby="propertyType-error" />
              )}
            />
            {getErrorMessage('propertyType') && <small id="propertyType-error" className="p-error">{getErrorMessage('propertyType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="propertyDescription">Property Description</label>
            <Controller name="propertyDescription" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="propertyDescription" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('propertyDescription') ? 'p-invalid' : ''} aria-describedby="propertyDescription-error" />
              )}
            />
            {getErrorMessage('propertyDescription') && <small id="propertyDescription-error" className="p-error">{getErrorMessage('propertyDescription')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="groupId">Group Id</label>
            <Controller name="groupId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="groupId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('groupId') ? 'p-invalid' : ''} aria-describedby="groupId-error" />
              )}
            />
            {getErrorMessage('groupId') && <small id="groupId-error" className="p-error">{getErrorMessage('groupId')}</small>}
          </div>
        </div>
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
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.propertyId && (
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

export default CoursePropertyForm;