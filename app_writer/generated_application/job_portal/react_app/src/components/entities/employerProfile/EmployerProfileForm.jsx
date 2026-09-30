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
import { createEmployerProfile } from '../../../store/slices/employerProfileSlice';
import { updateEmployerProfile } from '../../../store/slices/employerProfileSlice';
import logger from '../../../utils/logger';
import apiClient from '../../../services/apiClient';

const EmployerProfileForm = ({ data, onSave, onCancel, onNew, showForm = true, parentId }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/employer_profiles');
  const [myRecord, setMyRecord] = useState(null);
  const [myRecordLoading, setMyRecordLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      companyname: '',
      industry: '',
      website: '',
      logourl: '',
      description: '',
      contactemail: '',
    },
  });

  useEffect(() => {
    if (data) {
      reset({ ...data });
    }
  }, [data, reset]);



  useEffect(() => {
    let cancelled = false;
    const fetchMyRecord = async () => {
      try {
        const response = await apiClient.get('/api/employer_profiles/me');
        if (!cancelled && response.data) {
          setMyRecord(response.data);
          reset({ ...response.data });
          setEditMode(false);
        }
      } catch (err) {
        // 404 means no record yet — allow creation
        if (!cancelled) {
          setMyRecord(null);
          setEditMode(true);
        }
      } finally {
        if (!cancelled) setMyRecordLoading(false);
      }
    };
    fetchMyRecord();
    return () => { cancelled = true; };
  }, [reset]);


  const onSubmit = async (formData) => {
    const submitData = { ...formData, userProfileId: parentId };
    try {
      const existingId = myRecord?.employerProfileId;
      if (existingId) {
        await dispatch(updateEmployerProfile({ id: existingId, data: submitData })).unwrap();
      } else {
        const result = await dispatch(createEmployerProfile(submitData)).unwrap();
        setMyRecord(result);
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
      setEditMode(false);
    } catch (err) {
      logger.storeError('EmployerProfile save', err);
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
      {myRecordLoading ? (
        <div className="flex justify-content-center p-4"><i className="pi pi-spin pi-spinner" style={ { fontSize: '2rem' } } /></div>
      ) : (
      <>
      <div className="flex justify-content-end gap-2 mb-3">

      </div>
      {showForm && (
      <form onSubmit={handleSubmit(onSubmit)}>
      <div className="p-fluid">
      <div className="grid">
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="companyname">Companyname</label>
            <Controller name="companyname" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="companyname" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('companyname') ? 'p-invalid' : ''} aria-describedby="companyname-error" />
              )}
            />
            {getErrorMessage('companyname') && <small id="companyname-error" className="p-error">{getErrorMessage('companyname')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="industry">Industry</label>
            <Controller name="industry" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="industry" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('industry') ? 'p-invalid' : ''} aria-describedby="industry-error" />
              )}
            />
            {getErrorMessage('industry') && <small id="industry-error" className="p-error">{getErrorMessage('industry')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="website">Website</label>
            <Controller name="website" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="website" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('website') ? 'p-invalid' : ''} aria-describedby="website-error" />
              )}
            />
            {getErrorMessage('website') && <small id="website-error" className="p-error">{getErrorMessage('website')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="logourl">Logourl</label>
            <Controller name="logourl" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="logourl" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('logourl') ? 'p-invalid' : ''} aria-describedby="logourl-error" />
              )}
            />
            {getErrorMessage('logourl') && <small id="logourl-error" className="p-error">{getErrorMessage('logourl')}</small>}
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
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="contactemail">Contactemail</label>
            <Controller name="contactemail" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="contactemail" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('contactemail') ? 'p-invalid' : ''} aria-describedby="contactemail-error" />
              )}
            />
            {getErrorMessage('contactemail') && <small id="contactemail-error" className="p-error">{getErrorMessage('contactemail')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.employerProfileId && (
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
      </>
      )}
    </div>
  );
};

export default EmployerProfileForm;