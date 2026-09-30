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
import { createJobPostQuestion } from '../../../store/slices/jobPostQuestionSlice';
import { updateJobPostQuestion } from '../../../store/slices/jobPostQuestionSlice';
import logger from '../../../utils/logger';

const JobPostQuestionForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/jobpostquestions');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      jobPostId: null,
      questionText: '',
      questionType: '',
      isRequired: null,
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
      if (data?.questionId) {
        await dispatch(updateJobPostQuestion({ id: data.questionId, data: submitData })).unwrap();
      } else {
        await dispatch(createJobPostQuestion(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('JobPostQuestion save', err);
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="questionText">Question Text <span className="p-error">*</span></label>
            <Controller name="questionText" control={control} rules={ {required: 'Questiontext is required',} }
              render={({ field: f }) => (
                <InputText id="questionText" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('questionText') ? 'p-invalid' : ''} aria-describedby="questionText-error" />
              )}
            />
            {getErrorMessage('questionText') && <small id="questionText-error" className="p-error">{getErrorMessage('questionText')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="questionType">Question Type</label>
            <Controller name="questionType" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="questionType" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('questionType') ? 'p-invalid' : ''} aria-describedby="questionType-error" />
              )}
            />
            {getErrorMessage('questionType') && <small id="questionType-error" className="p-error">{getErrorMessage('questionType')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isRequired">Is Required</label>
            <Controller name="isRequired" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isRequired" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isRequired') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isRequired') && <small id="isRequired-error" className="p-error">{getErrorMessage('isRequired')}</small>}
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
        {!editMode && canUpdate && data?.questionId && (
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

export default JobPostQuestionForm;