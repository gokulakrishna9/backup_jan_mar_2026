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
import { createUserProfile } from '../../../store/slices/userProfileSlice';
import { updateUserProfile } from '../../../store/slices/userProfileSlice';
import logger from '../../../utils/logger';
import apiClient from '../../../services/apiClient';

const UserProfileForm = ({ data, onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/user_profiles');
  const [myRecord, setMyRecord] = useState(null);
  const [myRecordLoading, setMyRecordLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      firstname: '',
      lastname: '',
      email: '',
      phone: '',
      bio: '',
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
        const response = await apiClient.get('/api/user_profiles/me');
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
    const submitData = { ...formData };
    try {
      const existingId = myRecord?.userProfileId;
      if (existingId) {
        await dispatch(updateUserProfile({ id: existingId, data: submitData })).unwrap();
      } else {
        const result = await dispatch(createUserProfile(submitData)).unwrap();
        setMyRecord(result);
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
      setEditMode(false);
    } catch (err) {
      logger.storeError('UserProfile save', err);
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
            <label htmlFor="firstname">Firstname</label>
            <Controller name="firstname" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="firstname" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('firstname') ? 'p-invalid' : ''} aria-describedby="firstname-error" />
              )}
            />
            {getErrorMessage('firstname') && <small id="firstname-error" className="p-error">{getErrorMessage('firstname')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="lastname">Lastname</label>
            <Controller name="lastname" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="lastname" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('lastname') ? 'p-invalid' : ''} aria-describedby="lastname-error" />
              )}
            />
            {getErrorMessage('lastname') && <small id="lastname-error" className="p-error">{getErrorMessage('lastname')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="email">Email</label>
            <Controller name="email" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="email" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('email') ? 'p-invalid' : ''} aria-describedby="email-error" />
              )}
            />
            {getErrorMessage('email') && <small id="email-error" className="p-error">{getErrorMessage('email')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="phone">Phone</label>
            <Controller name="phone" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="phone" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('phone') ? 'p-invalid' : ''} aria-describedby="phone-error" />
              )}
            />
            {getErrorMessage('phone') && <small id="phone-error" className="p-error">{getErrorMessage('phone')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="bio">Bio</label>
            <Controller name="bio" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="bio" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('bio') ? 'p-invalid' : ''} aria-describedby="bio-error" />
              )}
            />
            {getErrorMessage('bio') && <small id="bio-error" className="p-error">{getErrorMessage('bio')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.userProfileId && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
        {canGrantAccess && data?.userProfileId && (
          <Button label="Grant Access" icon="pi pi-lock-open" className="p-button-warning p-ml-2" type="button" onClick={() => { /* Grant access handler */ }} />
        )}
      </div>
      </form>
      )}
      </>
      )}
    </div>
  );
};

export default UserProfileForm;