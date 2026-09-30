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
import { createCourseLesson } from '../../../store/slices/courseLessonSlice';
import { updateCourseLesson } from '../../../store/slices/courseLessonSlice';
import logger from '../../../utils/logger';

const CourseLessonForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/courselessons');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      moduleId: null,
      courseId: null,
      lessonTitle: '',
      lessonNumber: null,
      contentType: '',
      contentUrl: '',
      durationMinutes: null,
      isPreviewAvailable: null,
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
      if (data?.lessonId) {
        await dispatch(updateCourseLesson({ id: data.lessonId, data: submitData })).unwrap();
      } else {
        await dispatch(createCourseLesson(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CourseLesson save', err);
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
            <label htmlFor="moduleId">Module Id <span className="p-error">*</span></label>
            <Controller name="moduleId" control={control} rules={ {required: 'Moduleid is required',} }
              render={({ field: f }) => (
                <InputNumber id="moduleId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('moduleId') ? 'p-invalid' : ''} aria-describedby="moduleId-error" />
              )}
            />
            {getErrorMessage('moduleId') && <small id="moduleId-error" className="p-error">{getErrorMessage('moduleId')}</small>}
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="lessonTitle">Lesson Title <span className="p-error">*</span></label>
            <Controller name="lessonTitle" control={control} rules={ {required: 'Lessontitle is required',maxLength: { value: 255, message: 'Lessontitle cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="lessonTitle" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('lessonTitle') ? 'p-invalid' : ''} aria-describedby="lessonTitle-error" />
              )}
            />
            {getErrorMessage('lessonTitle') && <small id="lessonTitle-error" className="p-error">{getErrorMessage('lessonTitle')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="lessonNumber">Lesson Number <span className="p-error">*</span></label>
            <Controller name="lessonNumber" control={control} rules={ {required: 'Lessonnumber is required',} }
              render={({ field: f }) => (
                <InputNumber id="lessonNumber" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('lessonNumber') ? 'p-invalid' : ''} aria-describedby="lessonNumber-error" />
              )}
            />
            {getErrorMessage('lessonNumber') && <small id="lessonNumber-error" className="p-error">{getErrorMessage('lessonNumber')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="contentType">Content Type</label>
            <Controller name="contentType" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="contentType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('contentType') ? 'p-invalid' : ''} aria-describedby="contentType-error" />
              )}
            />
            {getErrorMessage('contentType') && <small id="contentType-error" className="p-error">{getErrorMessage('contentType')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="contentUrl">Content Url</label>
            <Controller name="contentUrl" control={control} rules={ {maxLength: { value: 500, message: 'Contenturl cannot exceed 500 characters' },} }
              render={({ field: f }) => (
                <InputText id="contentUrl" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('contentUrl') ? 'p-invalid' : ''} aria-describedby="contentUrl-error" />
              )}
            />
            {getErrorMessage('contentUrl') && <small id="contentUrl-error" className="p-error">{getErrorMessage('contentUrl')}</small>}
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
            <label htmlFor="isPreviewAvailable">Is Preview Available</label>
            <Controller name="isPreviewAvailable" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isPreviewAvailable" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isPreviewAvailable') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isPreviewAvailable') && <small id="isPreviewAvailable-error" className="p-error">{getErrorMessage('isPreviewAvailable')}</small>}
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
        {!editMode && canUpdate && data?.lessonId && (
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

export default CourseLessonForm;