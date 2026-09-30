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
import { createAiMarketTrendProperty } from '../../../store/slices/aiMarketTrendPropertySlice';
import { updateAiMarketTrendProperty } from '../../../store/slices/aiMarketTrendPropertySlice';
import logger from '../../../utils/logger';

const AiMarketTrendPropertyForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/aimarkettrendpropertys');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      trendName: '',
      trendDescription: '',
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
      if (data?.trendId) {
        await dispatch(updateAiMarketTrendProperty({ id: data.trendId, data: submitData })).unwrap();
      } else {
        await dispatch(createAiMarketTrendProperty(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('AiMarketTrendProperty save', err);
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="trendName">Trend Name <span className="p-error">*</span></label>
            <Controller name="trendName" control={control} rules={ {required: 'Trendname is required',maxLength: { value: 255, message: 'Trendname cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="trendName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('trendName') ? 'p-invalid' : ''} aria-describedby="trendName-error" />
              )}
            />
            {getErrorMessage('trendName') && <small id="trendName-error" className="p-error">{getErrorMessage('trendName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="trendDescription">Trend Description</label>
            <Controller name="trendDescription" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="trendDescription" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('trendDescription') ? 'p-invalid' : ''} aria-describedby="trendDescription-error" />
              )}
            />
            {getErrorMessage('trendDescription') && <small id="trendDescription-error" className="p-error">{getErrorMessage('trendDescription')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.trendId && (
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

export default AiMarketTrendPropertyForm;