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
import { createCourseAssignment } from '../../../store/slices/courseAssignmentSlice';
import { updateCourseAssignment } from '../../../store/slices/courseAssignmentSlice';
import logger from '../../../utils/logger';

const CourseAssignmentForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/courseassignments');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      courseId: null,
      moduleId: null,
      title: '',
      description: '',
      assignmentType: '',
      maxScore: null,
      passingScore: null,
      dueDate: null,
      durationMinutes: null,
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
      if (data?.assignmentId) {
        await dispatch(updateCourseAssignment({ id: data.assignmentId, data: submitData })).unwrap();
      } else {
        await dispatch(createCourseAssignment(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CourseAssignment save', err);
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
            <label htmlFor="moduleId">Module Id</label>
            <Controller name="moduleId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="moduleId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('moduleId') ? 'p-invalid' : ''} aria-describedby="moduleId-error" />
              )}
            />
            {getErrorMessage('moduleId') && <small id="moduleId-error" className="p-error">{getErrorMessage('moduleId')}</small>}
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
            <label htmlFor="assignmentType">Assignment Type</label>
            <Controller name="assignmentType" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="assignmentType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('assignmentType') ? 'p-invalid' : ''} aria-describedby="assignmentType-error" />
              )}
            />
            {getErrorMessage('assignmentType') && <small id="assignmentType-error" className="p-error">{getErrorMessage('assignmentType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="maxScore">Max Score <span className="p-error">*</span></label>
            <Controller name="maxScore" control={control} rules={ {required: 'Maxscore is required',} }
              render={({ field: f }) => (
                <InputNumber id="maxScore" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('maxScore') ? 'p-invalid' : ''} aria-describedby="maxScore-error" />
              )}
            />
            {getErrorMessage('maxScore') && <small id="maxScore-error" className="p-error">{getErrorMessage('maxScore')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="passingScore">Passing Score <span className="p-error">*</span></label>
            <Controller name="passingScore" control={control} rules={ {required: 'Passingscore is required',} }
              render={({ field: f }) => (
                <InputNumber id="passingScore" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('passingScore') ? 'p-invalid' : ''} aria-describedby="passingScore-error" />
              )}
            />
            {getErrorMessage('passingScore') && <small id="passingScore-error" className="p-error">{getErrorMessage('passingScore')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="dueDate">Due Date</label>
            <Controller name="dueDate" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="dueDate" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('dueDate') ? 'p-invalid' : ''} aria-describedby="dueDate-error" />
              )}
            />
            {getErrorMessage('dueDate') && <small id="dueDate-error" className="p-error">{getErrorMessage('dueDate')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="durationMinutes">Duration Minutes</label>
            <Controller name="durationMinutes" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="durationMinutes" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('durationMinutes') ? 'p-invalid' : ''} aria-describedby="durationMinutes-error" />
              )}
            />
            {getErrorMessage('durationMinutes') && <small id="durationMinutes-error" className="p-error">{getErrorMessage('durationMinutes')}</small>}
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
        {!editMode && canUpdate && data?.assignmentId && (
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

export default CourseAssignmentForm;