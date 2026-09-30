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
import { createCoursePrerequisite } from '../../../store/slices/coursePrerequisiteSlice';
import { updateCoursePrerequisite } from '../../../store/slices/coursePrerequisiteSlice';
import logger from '../../../utils/logger';

const CoursePrerequisiteForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/courseprerequisites');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      courseId: null,
      prerequisiteCourseId: null,
      prerequisiteType: '',
      prerequisiteDescription: '',
      isMandatory: null,
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
      if (data?.prerequisiteId) {
        await dispatch(updateCoursePrerequisite({ id: data.prerequisiteId, data: submitData })).unwrap();
      } else {
        await dispatch(createCoursePrerequisite(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CoursePrerequisite save', err);
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
            <label htmlFor="prerequisiteCourseId">Prerequisite Course Id</label>
            <Controller name="prerequisiteCourseId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="prerequisiteCourseId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('prerequisiteCourseId') ? 'p-invalid' : ''} aria-describedby="prerequisiteCourseId-error" />
              )}
            />
            {getErrorMessage('prerequisiteCourseId') && <small id="prerequisiteCourseId-error" className="p-error">{getErrorMessage('prerequisiteCourseId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="prerequisiteType">Prerequisite Type</label>
            <Controller name="prerequisiteType" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="prerequisiteType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('prerequisiteType') ? 'p-invalid' : ''} aria-describedby="prerequisiteType-error" />
              )}
            />
            {getErrorMessage('prerequisiteType') && <small id="prerequisiteType-error" className="p-error">{getErrorMessage('prerequisiteType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="prerequisiteDescription">Prerequisite Description</label>
            <Controller name="prerequisiteDescription" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="prerequisiteDescription" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('prerequisiteDescription') ? 'p-invalid' : ''} aria-describedby="prerequisiteDescription-error" />
              )}
            />
            {getErrorMessage('prerequisiteDescription') && <small id="prerequisiteDescription-error" className="p-error">{getErrorMessage('prerequisiteDescription')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isMandatory">Is Mandatory</label>
            <Controller name="isMandatory" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isMandatory" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isMandatory') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isMandatory') && <small id="isMandatory-error" className="p-error">{getErrorMessage('isMandatory')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.prerequisiteId && (
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

export default CoursePrerequisiteForm;