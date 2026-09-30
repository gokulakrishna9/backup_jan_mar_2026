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
import { createMarketTrendSkillDemand } from '../../../store/slices/marketTrendSkillDemandSlice';
import { updateMarketTrendSkillDemand } from '../../../store/slices/marketTrendSkillDemandSlice';
import logger from '../../../utils/logger';

const MarketTrendSkillDemandForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/markettrendskilldemands');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      trendId: null,
      skillName: '',
      demandLevel: '',
      growthRate: null,
      averageSalaryRange: '',
      jobOpeningsCount: null,
      region: '',
      industry: '',
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
      if (data?.demandId) {
        await dispatch(updateMarketTrendSkillDemand({ id: data.demandId, data: submitData })).unwrap();
      } else {
        await dispatch(createMarketTrendSkillDemand(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('MarketTrendSkillDemand save', err);
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
            <label htmlFor="skillName">Skill Name <span className="p-error">*</span></label>
            <Controller name="skillName" control={control} rules={ {required: 'Skillname is required',maxLength: { value: 255, message: 'Skillname cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="skillName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('skillName') ? 'p-invalid' : ''} aria-describedby="skillName-error" />
              )}
            />
            {getErrorMessage('skillName') && <small id="skillName-error" className="p-error">{getErrorMessage('skillName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="demandLevel">Demand Level</label>
            <Controller name="demandLevel" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="demandLevel" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('demandLevel') ? 'p-invalid' : ''} aria-describedby="demandLevel-error" />
              )}
            />
            {getErrorMessage('demandLevel') && <small id="demandLevel-error" className="p-error">{getErrorMessage('demandLevel')}</small>}
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
            <label htmlFor="averageSalaryRange">Average Salary Range</label>
            <Controller name="averageSalaryRange" control={control} rules={ {maxLength: { value: 100, message: 'Averagesalaryrange cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="averageSalaryRange" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('averageSalaryRange') ? 'p-invalid' : ''} aria-describedby="averageSalaryRange-error" />
              )}
            />
            {getErrorMessage('averageSalaryRange') && <small id="averageSalaryRange-error" className="p-error">{getErrorMessage('averageSalaryRange')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="jobOpeningsCount">Job Openings Count</label>
            <Controller name="jobOpeningsCount" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="jobOpeningsCount" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('jobOpeningsCount') ? 'p-invalid' : ''} aria-describedby="jobOpeningsCount-error" />
              )}
            />
            {getErrorMessage('jobOpeningsCount') && <small id="jobOpeningsCount-error" className="p-error">{getErrorMessage('jobOpeningsCount')}</small>}
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
            <label htmlFor="industry">Industry</label>
            <Controller name="industry" control={control} rules={ {maxLength: { value: 255, message: 'Industry cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="industry" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('industry') ? 'p-invalid' : ''} aria-describedby="industry-error" />
              )}
            />
            {getErrorMessage('industry') && <small id="industry-error" className="p-error">{getErrorMessage('industry')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.demandId && (
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

export default MarketTrendSkillDemandForm;