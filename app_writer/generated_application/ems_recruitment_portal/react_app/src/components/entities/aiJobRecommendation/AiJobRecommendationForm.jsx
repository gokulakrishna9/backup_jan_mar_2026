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
import { createAiJobRecommendation } from '../../../store/slices/aiJobRecommendationSlice';
import { updateAiJobRecommendation } from '../../../store/slices/aiJobRecommendationSlice';
import logger from '../../../utils/logger';

const AiJobRecommendationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/aijobrecommendations');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      jobPostId: null,
      profileId: null,
      preferenceRating: null,
      recommendationSummary: '',
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
      if (data?.preferenceId) {
        await dispatch(updateAiJobRecommendation({ id: data.preferenceId, data: submitData })).unwrap();
      } else {
        await dispatch(createAiJobRecommendation(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('AiJobRecommendation save', err);
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
            <label htmlFor="jobPostId">Job Post Id <span className="p-error">*</span></label>
            <Controller name="jobPostId" control={control} rules={ {required: 'Jobpostid is required',} }
              render={({ field: f }) => (
                <InputNumber id="jobPostId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('jobPostId') ? 'p-invalid' : ''} aria-describedby="jobPostId-error" />
              )}
            />
            {getErrorMessage('jobPostId') && <small id="jobPostId-error" className="p-error">{getErrorMessage('jobPostId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="profileId">Profile Id <span className="p-error">*</span></label>
            <Controller name="profileId" control={control} rules={ {required: 'Profileid is required',} }
              render={({ field: f }) => (
                <InputNumber id="profileId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('profileId') ? 'p-invalid' : ''} aria-describedby="profileId-error" />
              )}
            />
            {getErrorMessage('profileId') && <small id="profileId-error" className="p-error">{getErrorMessage('profileId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="preferenceRating">Preference Rating</label>
            <Controller name="preferenceRating" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="preferenceRating" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('preferenceRating') ? 'p-invalid' : ''} aria-describedby="preferenceRating-error" />
              )}
            />
            {getErrorMessage('preferenceRating') && <small id="preferenceRating-error" className="p-error">{getErrorMessage('preferenceRating')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="recommendationSummary">Recommendation Summary</label>
            <Controller name="recommendationSummary" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="recommendationSummary" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('recommendationSummary') ? 'p-invalid' : ''} aria-describedby="recommendationSummary-error" />
              )}
            />
            {getErrorMessage('recommendationSummary') && <small id="recommendationSummary-error" className="p-error">{getErrorMessage('recommendationSummary')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.preferenceId && (
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

export default AiJobRecommendationForm;