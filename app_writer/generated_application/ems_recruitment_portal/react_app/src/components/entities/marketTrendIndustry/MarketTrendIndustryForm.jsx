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
import { createMarketTrendIndustry } from '../../../store/slices/marketTrendIndustrySlice';
import { updateMarketTrendIndustry } from '../../../store/slices/marketTrendIndustrySlice';
import logger from '../../../utils/logger';

const MarketTrendIndustryForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/markettrendindustrys');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      trendId: null,
      industryName: '',
      description: '',
      growthRate: null,
      marketSize: '',
      emergingTechnologies: '',
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
      if (data?.industryId) {
        await dispatch(updateMarketTrendIndustry({ id: data.industryId, data: submitData })).unwrap();
      } else {
        await dispatch(createMarketTrendIndustry(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('MarketTrendIndustry save', err);
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
            <label htmlFor="trendId">Trend Id <span className="p-error">*</span></label>
            <Controller name="trendId" control={control} rules={ {required: 'Trendid is required',} }
              render={({ field: f }) => (
                <InputNumber id="trendId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('trendId') ? 'p-invalid' : ''} aria-describedby="trendId-error" />
              )}
            />
            {getErrorMessage('trendId') && <small id="trendId-error" className="p-error">{getErrorMessage('trendId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="industryName">Industry Name <span className="p-error">*</span></label>
            <Controller name="industryName" control={control} rules={ {required: 'Industryname is required',maxLength: { value: 255, message: 'Industryname cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="industryName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('industryName') ? 'p-invalid' : ''} aria-describedby="industryName-error" />
              )}
            />
            {getErrorMessage('industryName') && <small id="industryName-error" className="p-error">{getErrorMessage('industryName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="description">Description</label>
            <Controller name="description" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="description" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('description') ? 'p-invalid' : ''} aria-describedby="description-error" />
              )}
            />
            {getErrorMessage('description') && <small id="description-error" className="p-error">{getErrorMessage('description')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="growthRate">Growth Rate</label>
            <Controller name="growthRate" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="growthRate" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('growthRate') ? 'p-invalid' : ''} aria-describedby="growthRate-error" />
              )}
            />
            {getErrorMessage('growthRate') && <small id="growthRate-error" className="p-error">{getErrorMessage('growthRate')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="marketSize">Market Size</label>
            <Controller name="marketSize" control={control} rules={ {maxLength: { value: 100, message: 'Marketsize cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="marketSize" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('marketSize') ? 'p-invalid' : ''} aria-describedby="marketSize-error" />
              )}
            />
            {getErrorMessage('marketSize') && <small id="marketSize-error" className="p-error">{getErrorMessage('marketSize')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="emergingTechnologies">Emerging Technologies</label>
            <Controller name="emergingTechnologies" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="emergingTechnologies" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('emergingTechnologies') ? 'p-invalid' : ''} aria-describedby="emergingTechnologies-error" />
              )}
            />
            {getErrorMessage('emergingTechnologies') && <small id="emergingTechnologies-error" className="p-error">{getErrorMessage('emergingTechnologies')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.industryId && (
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

export default MarketTrendIndustryForm;