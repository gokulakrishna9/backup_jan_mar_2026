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
import { createCourseAnswer } from '../../../store/slices/courseAnswerSlice';
import { updateCourseAnswer } from '../../../store/slices/courseAnswerSlice';
import logger from '../../../utils/logger';

const CourseAnswerForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true, parentId }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/course_answers');
  const [editMode, setEditMode] = useState(mode === 'create');



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      answertext: '',
      answercode: '',
      isaccepted: null,
      upvotes: null,
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
    const submitData = { ...formData, courseQuestionId: parentId };
    try {
      if (data?.courseAnswerId) {
        await dispatch(updateCourseAnswer({ id: data.courseAnswerId, data: submitData })).unwrap();
      } else {
        await dispatch(createCourseAnswer(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CourseAnswer save', err);
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
            <label htmlFor="answertext">Answertext</label>
            <Controller name="answertext" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="answertext" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('answertext') ? 'p-invalid' : ''} aria-describedby="answertext-error" />
              )}
            />
            {getErrorMessage('answertext') && <small id="answertext-error" className="p-error">{getErrorMessage('answertext')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="answercode">Answercode</label>
            <Controller name="answercode" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="answercode" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('answercode') ? 'p-invalid' : ''} aria-describedby="answercode-error" />
              )}
            />
            {getErrorMessage('answercode') && <small id="answercode-error" className="p-error">{getErrorMessage('answercode')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isaccepted">Isaccepted</label>
            <Controller name="isaccepted" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isaccepted" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isaccepted') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isaccepted') && <small id="isaccepted-error" className="p-error">{getErrorMessage('isaccepted')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="upvotes">Upvotes</label>
            <Controller name="upvotes" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="upvotes" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('upvotes') ? 'p-invalid' : ''} aria-describedby="upvotes-error" />
              )}
            />
            {getErrorMessage('upvotes') && <small id="upvotes-error" className="p-error">{getErrorMessage('upvotes')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.courseAnswerId && (
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

export default CourseAnswerForm;