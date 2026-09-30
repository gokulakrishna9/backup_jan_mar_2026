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
import { createCourseDocumentGroup } from '../../../store/slices/courseDocumentGroupSlice';
import { updateCourseDocumentGroup } from '../../../store/slices/courseDocumentGroupSlice';
import logger from '../../../utils/logger';

const CourseDocumentGroupForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/coursedocumentgroups');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      groupName: '',
      groupDescription: '',
      courseId: null,
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
      if (data?.groupId) {
        await dispatch(updateCourseDocumentGroup({ id: data.groupId, data: submitData })).unwrap();
      } else {
        await dispatch(createCourseDocumentGroup(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CourseDocumentGroup save', err);
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
            <label htmlFor="groupName">Group Name <span className="p-error">*</span></label>
            <Controller name="groupName" control={control} rules={ {required: 'Groupname is required',maxLength: { value: 150, message: 'Groupname cannot exceed 150 characters' },} }
              render={({ field: f }) => (
                <InputText id="groupName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('groupName') ? 'p-invalid' : ''} aria-describedby="groupName-error" />
              )}
            />
            {getErrorMessage('groupName') && <small id="groupName-error" className="p-error">{getErrorMessage('groupName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="groupDescription">Group Description</label>
            <Controller name="groupDescription" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="groupDescription" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('groupDescription') ? 'p-invalid' : ''} aria-describedby="groupDescription-error" />
              )}
            />
            {getErrorMessage('groupDescription') && <small id="groupDescription-error" className="p-error">{getErrorMessage('groupDescription')}</small>}
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
        {!editMode && canUpdate && data?.groupId && (
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

export default CourseDocumentGroupForm;