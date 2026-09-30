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
import { createJobApplicationAnswer } from '../../../store/slices/jobApplicationAnswerSlice';
import { updateJobApplicationAnswer } from '../../../store/slices/jobApplicationAnswerSlice';
import logger from '../../../utils/logger';

const JobApplicationAnswerForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/jobapplicationanswers');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      applicationId: null,
      questionId: null,
      answerText: '',
      answerFileId: null,
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
      if (data?.answerId) {
        await dispatch(updateJobApplicationAnswer({ id: data.answerId, data: submitData })).unwrap();
      } else {
        await dispatch(createJobApplicationAnswer(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('JobApplicationAnswer save', err);
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
            <label htmlFor="applicationId">Application Id <span className="p-error">*</span></label>
            <Controller name="applicationId" control={control} rules={ {required: 'Applicationid is required',} }
              render={({ field: f }) => (
                <InputNumber id="applicationId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('applicationId') ? 'p-invalid' : ''} aria-describedby="applicationId-error" />
              )}
            />
            {getErrorMessage('applicationId') && <small id="applicationId-error" className="p-error">{getErrorMessage('applicationId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="questionId">Question Id <span className="p-error">*</span></label>
            <Controller name="questionId" control={control} rules={ {required: 'Questionid is required',} }
              render={({ field: f }) => (
                <InputNumber id="questionId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('questionId') ? 'p-invalid' : ''} aria-describedby="questionId-error" />
              )}
            />
            {getErrorMessage('questionId') && <small id="questionId-error" className="p-error">{getErrorMessage('questionId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="answerText">Answer Text</label>
            <Controller name="answerText" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="answerText" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('answerText') ? 'p-invalid' : ''} aria-describedby="answerText-error" />
              )}
            />
            {getErrorMessage('answerText') && <small id="answerText-error" className="p-error">{getErrorMessage('answerText')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="answerFileId">Answer File Id</label>
            <Controller name="answerFileId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="answerFileId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('answerFileId') ? 'p-invalid' : ''} aria-describedby="answerFileId-error" />
              )}
            />
            {getErrorMessage('answerFileId') && <small id="answerFileId-error" className="p-error">{getErrorMessage('answerFileId')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.answerId && (
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

export default JobApplicationAnswerForm;