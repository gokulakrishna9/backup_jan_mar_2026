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
import { createCourse } from '../../../store/slices/courseSlice';
import { updateCourse } from '../../../store/slices/courseSlice';
import logger from '../../../utils/logger';

const CourseForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/courses');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      courseName: '',
      description: '',
      outcomes: '',
      courseTypeId: null,
      isPublished: null,
      price: null,
      durationWeeks: null,
      institutionId: null,
      isEntity: null,
      isPublic: null,
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
      if (data?.courseId) {
        await dispatch(updateCourse({ id: data.courseId, data: submitData })).unwrap();
      } else {
        await dispatch(createCourse(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('Course save', err);
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
            <label htmlFor="courseName">Course Name <span className="p-error">*</span></label>
            <Controller name="courseName" control={control} rules={ {required: 'Coursename is required',maxLength: { value: 255, message: 'Coursename cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="courseName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('courseName') ? 'p-invalid' : ''} aria-describedby="courseName-error" />
              )}
            />
            {getErrorMessage('courseName') && <small id="courseName-error" className="p-error">{getErrorMessage('courseName')}</small>}
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
            <label htmlFor="outcomes">Outcomes</label>
            <Controller name="outcomes" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="outcomes" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('outcomes') ? 'p-invalid' : ''} aria-describedby="outcomes-error" />
              )}
            />
            {getErrorMessage('outcomes') && <small id="outcomes-error" className="p-error">{getErrorMessage('outcomes')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="courseTypeId">Course Type Id</label>
            <Controller name="courseTypeId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="courseTypeId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('courseTypeId') ? 'p-invalid' : ''} aria-describedby="courseTypeId-error" />
              )}
            />
            {getErrorMessage('courseTypeId') && <small id="courseTypeId-error" className="p-error">{getErrorMessage('courseTypeId')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isPublished">Is Published</label>
            <Controller name="isPublished" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isPublished" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isPublished') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isPublished') && <small id="isPublished-error" className="p-error">{getErrorMessage('isPublished')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="price">Price</label>
            <Controller name="price" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="price" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('price') ? 'p-invalid' : ''} aria-describedby="price-error" />
              )}
            />
            {getErrorMessage('price') && <small id="price-error" className="p-error">{getErrorMessage('price')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="durationWeeks">Duration Weeks</label>
            <Controller name="durationWeeks" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="durationWeeks" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('durationWeeks') ? 'p-invalid' : ''} aria-describedby="durationWeeks-error" />
              )}
            />
            {getErrorMessage('durationWeeks') && <small id="durationWeeks-error" className="p-error">{getErrorMessage('durationWeeks')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="institutionId">Institution Id</label>
            <Controller name="institutionId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="institutionId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('institutionId') ? 'p-invalid' : ''} aria-describedby="institutionId-error" />
              )}
            />
            {getErrorMessage('institutionId') && <small id="institutionId-error" className="p-error">{getErrorMessage('institutionId')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isEntity">Is Entity</label>
            <Controller name="isEntity" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isEntity" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isEntity') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isEntity') && <small id="isEntity-error" className="p-error">{getErrorMessage('isEntity')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isPublic">Is Public <span className="p-error">*</span></label>
            <Controller name="isPublic" control={control} rules={ {required: 'Ispublic is required',} }
              render={({ field: f }) => (
                <Checkbox id="isPublic" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isPublic') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isPublic') && <small id="isPublic-error" className="p-error">{getErrorMessage('isPublic')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.courseId && (
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

export default CourseForm;