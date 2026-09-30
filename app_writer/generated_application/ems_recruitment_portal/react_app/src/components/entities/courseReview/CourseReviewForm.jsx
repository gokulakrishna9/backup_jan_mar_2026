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
import { createCourseReview } from '../../../store/slices/courseReviewSlice';
import { updateCourseReview } from '../../../store/slices/courseReviewSlice';
import logger from '../../../utils/logger';

const CourseReviewForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/coursereviews');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      courseId: null,
      userId: null,
      rating: null,
      reviewTitle: '',
      reviewText: '',
      helpfulCount: null,
      isVerifiedPurchase: null,
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
      if (data?.reviewId) {
        await dispatch(updateCourseReview({ id: data.reviewId, data: submitData })).unwrap();
      } else {
        await dispatch(createCourseReview(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CourseReview save', err);
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
            <label htmlFor="rating">Rating <span className="p-error">*</span></label>
            <Controller name="rating" control={control} rules={ {required: 'Rating is required',} }
              render={({ field: f }) => (
                <InputNumber id="rating" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('rating') ? 'p-invalid' : ''} aria-describedby="rating-error" />
              )}
            />
            {getErrorMessage('rating') && <small id="rating-error" className="p-error">{getErrorMessage('rating')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="reviewTitle">Review Title</label>
            <Controller name="reviewTitle" control={control} rules={ {maxLength: { value: 255, message: 'Reviewtitle cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="reviewTitle" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('reviewTitle') ? 'p-invalid' : ''} aria-describedby="reviewTitle-error" />
              )}
            />
            {getErrorMessage('reviewTitle') && <small id="reviewTitle-error" className="p-error">{getErrorMessage('reviewTitle')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="reviewText">Review Text</label>
            <Controller name="reviewText" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="reviewText" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('reviewText') ? 'p-invalid' : ''} aria-describedby="reviewText-error" />
              )}
            />
            {getErrorMessage('reviewText') && <small id="reviewText-error" className="p-error">{getErrorMessage('reviewText')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="helpfulCount">Helpful Count</label>
            <Controller name="helpfulCount" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="helpfulCount" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('helpfulCount') ? 'p-invalid' : ''} aria-describedby="helpfulCount-error" />
              )}
            />
            {getErrorMessage('helpfulCount') && <small id="helpfulCount-error" className="p-error">{getErrorMessage('helpfulCount')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isVerifiedPurchase">Is Verified Purchase</label>
            <Controller name="isVerifiedPurchase" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isVerifiedPurchase" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isVerifiedPurchase') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isVerifiedPurchase') && <small id="isVerifiedPurchase-error" className="p-error">{getErrorMessage('isVerifiedPurchase')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.reviewId && (
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

export default CourseReviewForm;