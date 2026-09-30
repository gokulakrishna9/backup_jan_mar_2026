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
import { createExamQuestion } from '../../../store/slices/examQuestionSlice';
import { updateExamQuestion } from '../../../store/slices/examQuestionSlice';
import logger from '../../../utils/logger';

const ExamQuestionForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true, parentId }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/exam_questions');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      questiontext: '',
      questioncode: '',
      questiontype: '',
      points: null,
      sortorder: null,
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
    const submitData = { ...formData, trainingExamId: parentId };
    try {
      if (data?.examQuestionId) {
        await dispatch(updateExamQuestion({ id: data.examQuestionId, data: submitData })).unwrap();
      } else {
        await dispatch(createExamQuestion(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('ExamQuestion save', err);
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="questiontext">Questiontext</label>
            <Controller name="questiontext" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="questiontext" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('questiontext') ? 'p-invalid' : ''} aria-describedby="questiontext-error" />
              )}
            />
            {getErrorMessage('questiontext') && <small id="questiontext-error" className="p-error">{getErrorMessage('questiontext')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="questioncode">Questioncode</label>
            <Controller name="questioncode" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="questioncode" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('questioncode') ? 'p-invalid' : ''} aria-describedby="questioncode-error" />
              )}
            />
            {getErrorMessage('questioncode') && <small id="questioncode-error" className="p-error">{getErrorMessage('questioncode')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="questiontype">Questiontype</label>
            <Controller name="questiontype" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="questiontype" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('questiontype') ? 'p-invalid' : ''} aria-describedby="questiontype-error" />
              )}
            />
            {getErrorMessage('questiontype') && <small id="questiontype-error" className="p-error">{getErrorMessage('questiontype')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="points">Points</label>
            <Controller name="points" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="points" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('points') ? 'p-invalid' : ''} aria-describedby="points-error" />
              )}
            />
            {getErrorMessage('points') && <small id="points-error" className="p-error">{getErrorMessage('points')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="sortorder">Sortorder</label>
            <Controller name="sortorder" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="sortorder" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('sortorder') ? 'p-invalid' : ''} aria-describedby="sortorder-error" />
              )}
            />
            {getErrorMessage('sortorder') && <small id="sortorder-error" className="p-error">{getErrorMessage('sortorder')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.examQuestionId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
      </div>
      </form>
      )}
    </div>
  );
};

export default ExamQuestionForm;