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
import { createUserCourseProgress } from '../../../store/slices/userCourseProgressSlice';
import { updateUserCourseProgress } from '../../../store/slices/userCourseProgressSlice';
import logger from '../../../utils/logger';

const UserCourseProgressForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/usercourseprogresss');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      userId: null,
      courseId: null,
      lessonId: null,
      completionPercentage: null,
      lastAccessedAt: null,
      timeSpentMinutes: null,
      status: '',
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
      if (data?.progressId) {
        await dispatch(updateUserCourseProgress({ id: data.progressId, data: submitData })).unwrap();
      } else {
        await dispatch(createUserCourseProgress(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('UserCourseProgress save', err);
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
            <label htmlFor="userId">User Id <span className="p-error">*</span></label>
            <Controller name="userId" control={control} rules={ {required: 'Userid is required',} }
              render={({ field: f }) => (
                <InputNumber id="userId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('userId') ? 'p-invalid' : ''} aria-describedby="userId-error" />
              )}
            />
            {getErrorMessage('userId') && <small id="userId-error" className="p-error">{getErrorMessage('userId')}</small>}
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
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="lessonId">Lesson Id</label>
            <Controller name="lessonId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="lessonId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('lessonId') ? 'p-invalid' : ''} aria-describedby="lessonId-error" />
              )}
            />
            {getErrorMessage('lessonId') && <small id="lessonId-error" className="p-error">{getErrorMessage('lessonId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="completionPercentage">Completion Percentage</label>
            <Controller name="completionPercentage" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="completionPercentage" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('completionPercentage') ? 'p-invalid' : ''} aria-describedby="completionPercentage-error" />
              )}
            />
            {getErrorMessage('completionPercentage') && <small id="completionPercentage-error" className="p-error">{getErrorMessage('completionPercentage')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="lastAccessedAt">Last Accessed At</label>
            <Controller name="lastAccessedAt" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="lastAccessedAt" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('lastAccessedAt') ? 'p-invalid' : ''} aria-describedby="lastAccessedAt-error" />
              )}
            />
            {getErrorMessage('lastAccessedAt') && <small id="lastAccessedAt-error" className="p-error">{getErrorMessage('lastAccessedAt')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="timeSpentMinutes">Time Spent Minutes</label>
            <Controller name="timeSpentMinutes" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="timeSpentMinutes" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('timeSpentMinutes') ? 'p-invalid' : ''} aria-describedby="timeSpentMinutes-error" />
              )}
            />
            {getErrorMessage('timeSpentMinutes') && <small id="timeSpentMinutes-error" className="p-error">{getErrorMessage('timeSpentMinutes')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="status">Status</label>
            <Controller name="status" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="status" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('status') ? 'p-invalid' : ''} aria-describedby="status-error" />
              )}
            />
            {getErrorMessage('status') && <small id="status-error" className="p-error">{getErrorMessage('status')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.progressId && (
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

export default UserCourseProgressForm;