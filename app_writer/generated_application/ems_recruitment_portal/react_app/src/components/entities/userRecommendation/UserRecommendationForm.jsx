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
import { createUserRecommendation } from '../../../store/slices/userRecommendationSlice';
import { updateUserRecommendation } from '../../../store/slices/userRecommendationSlice';
import logger from '../../../utils/logger';

const UserRecommendationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/userrecommendations');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      userId: null,
      recommendedByUserId: null,
      recommendationText: '',
      relationship: '',
      positionAtTime: '',
      isVisible: null,
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
      if (data?.recommendationId) {
        await dispatch(updateUserRecommendation({ id: data.recommendationId, data: submitData })).unwrap();
      } else {
        await dispatch(createUserRecommendation(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('UserRecommendation save', err);
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
            <label htmlFor="recommendedByUserId">Recommended By User Id <span className="p-error">*</span></label>
            <Controller name="recommendedByUserId" control={control} rules={ {required: 'Recommendedbyuserid is required',} }
              render={({ field: f }) => (
                <InputNumber id="recommendedByUserId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('recommendedByUserId') ? 'p-invalid' : ''} aria-describedby="recommendedByUserId-error" />
              )}
            />
            {getErrorMessage('recommendedByUserId') && <small id="recommendedByUserId-error" className="p-error">{getErrorMessage('recommendedByUserId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="recommendationText">Recommendation Text <span className="p-error">*</span></label>
            <Controller name="recommendationText" control={control} rules={ {required: 'Recommendationtext is required',} }
              render={({ field: f }) => (
                <InputText id="recommendationText" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('recommendationText') ? 'p-invalid' : ''} aria-describedby="recommendationText-error" />
              )}
            />
            {getErrorMessage('recommendationText') && <small id="recommendationText-error" className="p-error">{getErrorMessage('recommendationText')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="relationship">Relationship</label>
            <Controller name="relationship" control={control} rules={ {maxLength: { value: 100, message: 'Relationship cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="relationship" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('relationship') ? 'p-invalid' : ''} aria-describedby="relationship-error" />
              )}
            />
            {getErrorMessage('relationship') && <small id="relationship-error" className="p-error">{getErrorMessage('relationship')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="positionAtTime">Position At Time</label>
            <Controller name="positionAtTime" control={control} rules={ {maxLength: { value: 255, message: 'Positionattime cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="positionAtTime" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('positionAtTime') ? 'p-invalid' : ''} aria-describedby="positionAtTime-error" />
              )}
            />
            {getErrorMessage('positionAtTime') && <small id="positionAtTime-error" className="p-error">{getErrorMessage('positionAtTime')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isVisible">Is Visible</label>
            <Controller name="isVisible" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isVisible" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isVisible') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isVisible') && <small id="isVisible-error" className="p-error">{getErrorMessage('isVisible')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.recommendationId && (
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

export default UserRecommendationForm;