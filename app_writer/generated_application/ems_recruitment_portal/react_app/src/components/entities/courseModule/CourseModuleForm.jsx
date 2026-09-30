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
import { createCourseModule } from '../../../store/slices/courseModuleSlice';
import { updateCourseModule } from '../../../store/slices/courseModuleSlice';
import logger from '../../../utils/logger';

const CourseModuleForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/coursemodules');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      courseId: null,
      moduleName: '',
      moduleNumber: null,
      description: '',
      durationHours: null,
      learningObjectives: '',
      isMandatory: null,
      orderSequence: null,
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
      if (data?.moduleId) {
        await dispatch(updateCourseModule({ id: data.moduleId, data: submitData })).unwrap();
      } else {
        await dispatch(createCourseModule(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CourseModule save', err);
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="moduleName">Module Name <span className="p-error">*</span></label>
            <Controller name="moduleName" control={control} rules={ {required: 'Modulename is required',maxLength: { value: 255, message: 'Modulename cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="moduleName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('moduleName') ? 'p-invalid' : ''} aria-describedby="moduleName-error" />
              )}
            />
            {getErrorMessage('moduleName') && <small id="moduleName-error" className="p-error">{getErrorMessage('moduleName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="moduleNumber">Module Number <span className="p-error">*</span></label>
            <Controller name="moduleNumber" control={control} rules={ {required: 'Modulenumber is required',} }
              render={({ field: f }) => (
                <InputNumber id="moduleNumber" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('moduleNumber') ? 'p-invalid' : ''} aria-describedby="moduleNumber-error" />
              )}
            />
            {getErrorMessage('moduleNumber') && <small id="moduleNumber-error" className="p-error">{getErrorMessage('moduleNumber')}</small>}
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
            <label htmlFor="durationHours">Duration Hours</label>
            <Controller name="durationHours" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="durationHours" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('durationHours') ? 'p-invalid' : ''} aria-describedby="durationHours-error" />
              )}
            />
            {getErrorMessage('durationHours') && <small id="durationHours-error" className="p-error">{getErrorMessage('durationHours')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="learningObjectives">Learning Objectives</label>
            <Controller name="learningObjectives" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="learningObjectives" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('learningObjectives') ? 'p-invalid' : ''} aria-describedby="learningObjectives-error" />
              )}
            />
            {getErrorMessage('learningObjectives') && <small id="learningObjectives-error" className="p-error">{getErrorMessage('learningObjectives')}</small>}
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
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="orderSequence">Order Sequence <span className="p-error">*</span></label>
            <Controller name="orderSequence" control={control} rules={ {required: 'Ordersequence is required',} }
              render={({ field: f }) => (
                <InputNumber id="orderSequence" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('orderSequence') ? 'p-invalid' : ''} aria-describedby="orderSequence-error" />
              )}
            />
            {getErrorMessage('orderSequence') && <small id="orderSequence-error" className="p-error">{getErrorMessage('orderSequence')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.moduleId && (
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

export default CourseModuleForm;