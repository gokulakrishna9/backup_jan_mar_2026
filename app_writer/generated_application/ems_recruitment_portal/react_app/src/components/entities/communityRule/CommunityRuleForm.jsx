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
import { createCommunityRule } from '../../../store/slices/communityRuleSlice';
import { updateCommunityRule } from '../../../store/slices/communityRuleSlice';
import logger from '../../../utils/logger';

const CommunityRuleForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/communityrules');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      communityId: null,
      ruleTitle: '',
      ruleDescription: '',
      orderSequence: null,
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
      if (data?.ruleId) {
        await dispatch(updateCommunityRule({ id: data.ruleId, data: submitData })).unwrap();
      } else {
        await dispatch(createCommunityRule(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('CommunityRule save', err);
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
            <label htmlFor="communityId">Community Id <span className="p-error">*</span></label>
            <Controller name="communityId" control={control} rules={ {required: 'Communityid is required',} }
              render={({ field: f }) => (
                <InputNumber id="communityId" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('communityId') ? 'p-invalid' : ''} aria-describedby="communityId-error" />
              )}
            />
            {getErrorMessage('communityId') && <small id="communityId-error" className="p-error">{getErrorMessage('communityId')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="ruleTitle">Rule Title <span className="p-error">*</span></label>
            <Controller name="ruleTitle" control={control} rules={ {required: 'Ruletitle is required',maxLength: { value: 255, message: 'Ruletitle cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="ruleTitle" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('ruleTitle') ? 'p-invalid' : ''} aria-describedby="ruleTitle-error" />
              )}
            />
            {getErrorMessage('ruleTitle') && <small id="ruleTitle-error" className="p-error">{getErrorMessage('ruleTitle')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="ruleDescription">Rule Description <span className="p-error">*</span></label>
            <Controller name="ruleDescription" control={control} rules={ {required: 'Ruledescription is required',} }
              render={({ field: f }) => (
                <InputText id="ruleDescription" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('ruleDescription') ? 'p-invalid' : ''} aria-describedby="ruleDescription-error" />
              )}
            />
            {getErrorMessage('ruleDescription') && <small id="ruleDescription-error" className="p-error">{getErrorMessage('ruleDescription')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="orderSequence">Order Sequence <span className="p-error">*</span></label>
            <Controller name="orderSequence" control={control} rules={ {required: 'Ordersequence is required',} }
              render={({ field: f }) => (
                <InputNumber id="orderSequence" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('orderSequence') ? 'p-invalid' : ''} aria-describedby="orderSequence-error" />
              )}
            />
            {getErrorMessage('orderSequence') && <small id="orderSequence-error" className="p-error">{getErrorMessage('orderSequence')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.ruleId && (
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

export default CommunityRuleForm;