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
import { createExamAttempt } from '../../../store/slices/examAttemptSlice';
import { updateExamAttempt } from '../../../store/slices/examAttemptSlice';
import logger from '../../../utils/logger';

const ExamAttemptForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/exam_attempts');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      score: null,
      passed: null,
      startedat: null,
      completedat: null,
      attemptnumber: null,
    },
  });

  useEffect(() => {
    if (data) {
      reset({ ...data });
    }
  }, [data, reset]);

  useEffect(() => {
    setEditMode(mode === 'create' || mode === 'edit');
  }, [mode]);



  const onSubmit = async (formData) => {
    const submitData = { ...formData };
    try {
      if (data?.examAttemptId) {
        await dispatch(updateExamAttempt({ id: data.examAttemptId, data: submitData })).unwrap();
      } else {
        await dispatch(createExamAttempt(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('ExamAttempt save', err);
      toast.current?.show({ severity: 'error', summary: 'Error', detail: String(err), life: 5000 });
    }
  };

  const isDisabled = !editMode;

  const colsLg = 3;
  const colsMd = 2;
  const colsSm = 1;
  const fullWidthTypes = ['InputTextarea', 'QuillEditor', 'MonacoEditor', 'MarkdownEditor', 'FileUpload'];


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
          <Button label="New" icon="pi pi-plus" className="p-button-success p-button-sm" onClick={() => { reset({}); setEditMode(true); if (onNew) onNew(); }} />
        )}
      </div>
      {showForm && (
      <form onSubmit={handleSubmit(onSubmit)}>
      <div className="p-fluid">
      <div className="grid">
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
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="passed">Passed</label>
            <Controller name="passed" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="passed" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('passed') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('passed') && <small id="passed-error" className="p-error">{getErrorMessage('passed')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="startedat">Startedat</label>
            <Controller name="startedat" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="startedat" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('startedat') ? 'p-invalid' : ''} aria-describedby="startedat-error" />
              )}
            />
            {getErrorMessage('startedat') && <small id="startedat-error" className="p-error">{getErrorMessage('startedat')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="completedat">Completedat</label>
            <Controller name="completedat" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="completedat" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} showTime className={getErrorMessage('completedat') ? 'p-invalid' : ''} aria-describedby="completedat-error" />
              )}
            />
            {getErrorMessage('completedat') && <small id="completedat-error" className="p-error">{getErrorMessage('completedat')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="attemptnumber">Attemptnumber</label>
            <Controller name="attemptnumber" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="attemptnumber" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('attemptnumber') ? 'p-invalid' : ''} aria-describedby="attemptnumber-error" />
              )}
            />
            {getErrorMessage('attemptnumber') && <small id="attemptnumber-error" className="p-error">{getErrorMessage('attemptnumber')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.examAttemptId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
        {canGrantAccess && data?.examAttemptId && (
          <Button label="Grant Access" icon="pi pi-lock-open" className="p-button-warning p-ml-2" type="button" onClick={() => { /* Grant access handler */ }} />
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default ExamAttemptForm;