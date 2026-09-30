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
import { createMarketTrendLocation } from '../../../store/slices/marketTrendLocationSlice';
import { updateMarketTrendLocation } from '../../../store/slices/marketTrendLocationSlice';
import logger from '../../../utils/logger';

const MarketTrendLocationForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/markettrendlocations');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      trendId: null,
      country: '',
      region: '',
      city: '',
      jobMarketHealth: '',
      unemploymentRate: null,
      averageSalary: '',
      costOfLivingIndex: null,
      topIndustries: '',
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
      if (data?.locationId) {
        await dispatch(updateMarketTrendLocation({ id: data.locationId, data: submitData })).unwrap();
      } else {
        await dispatch(createMarketTrendLocation(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('MarketTrendLocation save', err);
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
            <label htmlFor="country">Country <span className="p-error">*</span></label>
            <Controller name="country" control={control} rules={ {required: 'Country is required',maxLength: { value: 100, message: 'Country cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="country" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('country') ? 'p-invalid' : ''} aria-describedby="country-error" />
              )}
            />
            {getErrorMessage('country') && <small id="country-error" className="p-error">{getErrorMessage('country')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="region">Region</label>
            <Controller name="region" control={control} rules={ {maxLength: { value: 255, message: 'Region cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="region" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('region') ? 'p-invalid' : ''} aria-describedby="region-error" />
              )}
            />
            {getErrorMessage('region') && <small id="region-error" className="p-error">{getErrorMessage('region')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="city">City</label>
            <Controller name="city" control={control} rules={ {maxLength: { value: 100, message: 'City cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="city" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('city') ? 'p-invalid' : ''} aria-describedby="city-error" />
              )}
            />
            {getErrorMessage('city') && <small id="city-error" className="p-error">{getErrorMessage('city')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="jobMarketHealth">Job Market Health</label>
            <Controller name="jobMarketHealth" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="jobMarketHealth" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('jobMarketHealth') ? 'p-invalid' : ''} aria-describedby="jobMarketHealth-error" />
              )}
            />
            {getErrorMessage('jobMarketHealth') && <small id="jobMarketHealth-error" className="p-error">{getErrorMessage('jobMarketHealth')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="unemploymentRate">Unemployment Rate</label>
            <Controller name="unemploymentRate" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="unemploymentRate" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('unemploymentRate') ? 'p-invalid' : ''} aria-describedby="unemploymentRate-error" />
              )}
            />
            {getErrorMessage('unemploymentRate') && <small id="unemploymentRate-error" className="p-error">{getErrorMessage('unemploymentRate')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="averageSalary">Average Salary</label>
            <Controller name="averageSalary" control={control} rules={ {maxLength: { value: 100, message: 'Averagesalary cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="averageSalary" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('averageSalary') ? 'p-invalid' : ''} aria-describedby="averageSalary-error" />
              )}
            />
            {getErrorMessage('averageSalary') && <small id="averageSalary-error" className="p-error">{getErrorMessage('averageSalary')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="costOfLivingIndex">Cost Of Living Index</label>
            <Controller name="costOfLivingIndex" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="costOfLivingIndex" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('costOfLivingIndex') ? 'p-invalid' : ''} aria-describedby="costOfLivingIndex-error" />
              )}
            />
            {getErrorMessage('costOfLivingIndex') && <small id="costOfLivingIndex-error" className="p-error">{getErrorMessage('costOfLivingIndex')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="topIndustries">Top Industries</label>
            <Controller name="topIndustries" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="topIndustries" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('topIndustries') ? 'p-invalid' : ''} aria-describedby="topIndustries-error" />
              )}
            />
            {getErrorMessage('topIndustries') && <small id="topIndustries-error" className="p-error">{getErrorMessage('topIndustries')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.locationId && (
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

export default MarketTrendLocationForm;