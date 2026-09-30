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
import { createUserAssignmentSubmission } from '../../../store/slices/userAssignmentSubmissionSlice';
import { updateUserAssignmentSubmission } from '../../../store/slices/userAssignmentSubmissionSlice';
import logger from '../../../utils/logger';

const UserAssignmentSubmissionForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/userassignmentsubmissions');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      assignmentId: null,
      userId: null,
      submissionContent: '',
      submissionFileId: null,
      submittedAt: null,
      score: null,
      feedback: '',
      gradedByUserId: null,
      gradedAt: null,
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
      if (data?.submissionId) {
        await dispatch(updateUserAssignmentSubmission({ id: data.submissionId, data: submitData })).unwrap();
      } else {
        await dispatch(createUserAssignmentSubmission(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('UserAssignmentSubmission save', err);
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
            <label htmlFor="assignmentId">Assignment Id <span className="p-error">*</span></label>
            <Controller name="assignmentId" control={control} rules={ {required: 'Assignmentid is required',} }
              render={({ field: f }) => (
                <InputNumber id="assignmentId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('assignmentId') ? 'p-invalid' : ''} aria-describedby="assignmentId-error" />
              )}
            />
            {getErrorMessage('assignmentId') && <small id="assignmentId-error" className="p-error">{getErrorMessage('assignmentId')}</small>}
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="submissionContent">Submission Content</label>
            <Controller name="submissionContent" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="submissionContent" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('submissionContent') ? 'p-invalid' : ''} aria-describedby="submissionContent-error" />
              )}
            />
            {getErrorMessage('submissionContent') && <small id="submissionContent-error" className="p-error">{getErrorMessage('submissionContent')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="submissionFileId">Submission File Id</label>
            <Controller name="submissionFileId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="submissionFileId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('submissionFileId') ? 'p-invalid' : ''} aria-describedby="submissionFileId-error" />
              )}
            />
            {getErrorMessage('submissionFileId') && <small id="submissionFileId-error" className="p-error">{getErrorMessage('submissionFileId')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="submittedAt">Submitted At</label>
            <Controller name="submittedAt" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="submittedAt" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('submittedAt') ? 'p-invalid' : ''} aria-describedby="submittedAt-error" />
              )}
            />
            {getErrorMessage('submittedAt') && <small id="submittedAt-error" className="p-error">{getErrorMessage('submittedAt')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="score">Score</label>
            <Controller name="score" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="score" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('score') ? 'p-invalid' : ''} aria-describedby="score-error" />
              )}
            />
            {getErrorMessage('score') && <small id="score-error" className="p-error">{getErrorMessage('score')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="feedback">Feedback</label>
            <Controller name="feedback" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="feedback" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('feedback') ? 'p-invalid' : ''} aria-describedby="feedback-error" />
              )}
            />
            {getErrorMessage('feedback') && <small id="feedback-error" className="p-error">{getErrorMessage('feedback')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="gradedByUserId">Graded By User Id</label>
            <Controller name="gradedByUserId" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="gradedByUserId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('gradedByUserId') ? 'p-invalid' : ''} aria-describedby="gradedByUserId-error" />
              )}
            />
            {getErrorMessage('gradedByUserId') && <small id="gradedByUserId-error" className="p-error">{getErrorMessage('gradedByUserId')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="gradedAt">Graded At</label>
            <Controller name="gradedAt" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="gradedAt" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('gradedAt') ? 'p-invalid' : ''} aria-describedby="gradedAt-error" />
              )}
            />
            {getErrorMessage('gradedAt') && <small id="gradedAt-error" className="p-error">{getErrorMessage('gradedAt')}</small>}
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
        {!editMode && canUpdate && data?.submissionId && (
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

export default UserAssignmentSubmissionForm;