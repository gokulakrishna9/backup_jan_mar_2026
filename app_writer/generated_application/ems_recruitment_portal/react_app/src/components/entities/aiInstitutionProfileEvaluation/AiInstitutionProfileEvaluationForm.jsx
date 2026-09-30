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
import { createAiInstitutionProfileEvaluation } from '../../../store/slices/aiInstitutionProfileEvaluationSlice';
import { updateAiInstitutionProfileEvaluation } from '../../../store/slices/aiInstitutionProfileEvaluationSlice';
import logger from '../../../utils/logger';

const AiInstitutionProfileEvaluationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/aiinstitutionprofileevaluations');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      institutionId: null,
      evaluationSummary: '',
      rating: null,
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
      if (data?.evaluationId) {
        await dispatch(updateAiInstitutionProfileEvaluation({ id: data.evaluationId, data: submitData })).unwrap();
      } else {
        await dispatch(createAiInstitutionProfileEvaluation(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('AiInstitutionProfileEvaluation save', err);
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
            <label htmlFor="institutionId">Institution Id <span className="p-error">*</span></label>
            <Controller name="institutionId" control={control} rules={ {required: 'Institutionid is required',} }
              render={({ field: f }) => (
                <InputNumber id="institutionId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('institutionId') ? 'p-invalid' : ''} aria-describedby="institutionId-error" />
              )}
            />
            {getErrorMessage('institutionId') && <small id="institutionId-error" className="p-error">{getErrorMessage('institutionId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="evaluationSummary">Evaluation Summary</label>
            <Controller name="evaluationSummary" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="evaluationSummary" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('evaluationSummary') ? 'p-invalid' : ''} aria-describedby="evaluationSummary-error" />
              )}
            />
            {getErrorMessage('evaluationSummary') && <small id="evaluationSummary-error" className="p-error">{getErrorMessage('evaluationSummary')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="rating">Rating</label>
            <Controller name="rating" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="rating" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('rating') ? 'p-invalid' : ''} aria-describedby="rating-error" />
              )}
            />
            {getErrorMessage('rating') && <small id="rating-error" className="p-error">{getErrorMessage('rating')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.evaluationId && (
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

export default AiInstitutionProfileEvaluationForm;