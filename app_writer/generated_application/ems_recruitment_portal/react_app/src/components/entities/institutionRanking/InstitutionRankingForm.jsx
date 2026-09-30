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
import { createInstitutionRanking } from '../../../store/slices/institutionRankingSlice';
import { updateInstitutionRanking } from '../../../store/slices/institutionRankingSlice';
import logger from '../../../utils/logger';

const InstitutionRankingForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/institutionrankings');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      institutionId: null,
      rankingOrganization: '',
      rankingYear: null,
      overallRank: null,
      countryRank: null,
      category: '',
      categoryRank: null,
      score: null,
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
      if (data?.rankingId) {
        await dispatch(updateInstitutionRanking({ id: data.rankingId, data: submitData })).unwrap();
      } else {
        await dispatch(createInstitutionRanking(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('InstitutionRanking save', err);
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
            <label htmlFor="institutionId">Institution Id <span className="p-error">*</span></label>
            <Controller name="institutionId" control={control} rules={ {required: 'Institutionid is required',} }
              render={({ field: f }) => (
                <InputNumber id="institutionId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('institutionId') ? 'p-invalid' : ''} aria-describedby="institutionId-error" />
              )}
            />
            {getErrorMessage('institutionId') && <small id="institutionId-error" className="p-error">{getErrorMessage('institutionId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="rankingOrganization">Ranking Organization <span className="p-error">*</span></label>
            <Controller name="rankingOrganization" control={control} rules={ {required: 'Rankingorganization is required',maxLength: { value: 255, message: 'Rankingorganization cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="rankingOrganization" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('rankingOrganization') ? 'p-invalid' : ''} aria-describedby="rankingOrganization-error" />
              )}
            />
            {getErrorMessage('rankingOrganization') && <small id="rankingOrganization-error" className="p-error">{getErrorMessage('rankingOrganization')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="rankingYear">Ranking Year <span className="p-error">*</span></label>
            <Controller name="rankingYear" control={control} rules={ {required: 'Rankingyear is required',} }
              render={({ field: f }) => (
                <InputNumber id="rankingYear" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('rankingYear') ? 'p-invalid' : ''} aria-describedby="rankingYear-error" />
              )}
            />
            {getErrorMessage('rankingYear') && <small id="rankingYear-error" className="p-error">{getErrorMessage('rankingYear')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="overallRank">Overall Rank</label>
            <Controller name="overallRank" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="overallRank" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('overallRank') ? 'p-invalid' : ''} aria-describedby="overallRank-error" />
              )}
            />
            {getErrorMessage('overallRank') && <small id="overallRank-error" className="p-error">{getErrorMessage('overallRank')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="countryRank">Country Rank</label>
            <Controller name="countryRank" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="countryRank" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('countryRank') ? 'p-invalid' : ''} aria-describedby="countryRank-error" />
              )}
            />
            {getErrorMessage('countryRank') && <small id="countryRank-error" className="p-error">{getErrorMessage('countryRank')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="category">Category</label>
            <Controller name="category" control={control} rules={ {maxLength: { value: 255, message: 'Category cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="category" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('category') ? 'p-invalid' : ''} aria-describedby="category-error" />
              )}
            />
            {getErrorMessage('category') && <small id="category-error" className="p-error">{getErrorMessage('category')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="categoryRank">Category Rank</label>
            <Controller name="categoryRank" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="categoryRank" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('categoryRank') ? 'p-invalid' : ''} aria-describedby="categoryRank-error" />
              )}
            />
            {getErrorMessage('categoryRank') && <small id="categoryRank-error" className="p-error">{getErrorMessage('categoryRank')}</small>}
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
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.rankingId && (
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

export default InstitutionRankingForm;