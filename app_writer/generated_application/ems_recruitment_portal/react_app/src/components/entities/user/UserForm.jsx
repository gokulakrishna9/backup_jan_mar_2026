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
import { createUser } from '../../../store/slices/userSlice';
import { updateUser } from '../../../store/slices/userSlice';
import logger from '../../../utils/logger';

const UserForm = ({ data, mode = 'view', onSave, onCancel, onNew, showForm = true }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/users');
  const [editMode, setEditMode] = useState(mode === 'create');


  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      firstName: '',
      lastName: '',
      gender: '',
      dateOfBirth: null,
      emailAddress: '',
      userName: '',
      encryptedPassword: '',
      phoneNumber: '',
      profilePhoto: '',
      isActive: null,
      isEntity: null,
      isPublic: null,
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
      if (data?.userId) {
        await dispatch(updateUser({ id: data.userId, data: submitData })).unwrap();
      } else {
        await dispatch(createUser(submitData)).unwrap();
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
    } catch (err) {
      logger.storeError('User save', err);
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
            <label htmlFor="firstName">First Name <span className="p-error">*</span></label>
            <Controller name="firstName" control={control} rules={ {required: 'Firstname is required',maxLength: { value: 100, message: 'Firstname cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="firstName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('firstName') ? 'p-invalid' : ''} aria-describedby="firstName-error" />
              )}
            />
            {getErrorMessage('firstName') && <small id="firstName-error" className="p-error">{getErrorMessage('firstName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="lastName">Last Name <span className="p-error">*</span></label>
            <Controller name="lastName" control={control} rules={ {required: 'Lastname is required',maxLength: { value: 100, message: 'Lastname cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="lastName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('lastName') ? 'p-invalid' : ''} aria-describedby="lastName-error" />
              )}
            />
            {getErrorMessage('lastName') && <small id="lastName-error" className="p-error">{getErrorMessage('lastName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="gender">Gender</label>
            <Controller name="gender" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="gender" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('gender') ? 'p-invalid' : ''} aria-describedby="gender-error" />
              )}
            />
            {getErrorMessage('gender') && <small id="gender-error" className="p-error">{getErrorMessage('gender')}</small>}
          </div>
        </div>
        <div className={getColClass('Calendar')}>
          <div className="field p-mb-3">
            <label htmlFor="dateOfBirth">Date Of Birth</label>
            <Controller name="dateOfBirth" control={control} rules={ {} }
              render={({ field: f }) => (
                <Calendar id="dateOfBirth" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('dateOfBirth') ? 'p-invalid' : ''} aria-describedby="dateOfBirth-error" />
              )}
            />
            {getErrorMessage('dateOfBirth') && <small id="dateOfBirth-error" className="p-error">{getErrorMessage('dateOfBirth')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="emailAddress">Email Address <span className="p-error">*</span></label>
            <Controller name="emailAddress" control={control} rules={ {required: 'Emailaddress is required',maxLength: { value: 255, message: 'Emailaddress cannot exceed 255 characters' },pattern: { value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: 'Please provide a valid email address' },} }
              render={({ field: f }) => (
                <InputText id="emailAddress" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('emailAddress') ? 'p-invalid' : ''} aria-describedby="emailAddress-error" />
              )}
            />
            {getErrorMessage('emailAddress') && <small id="emailAddress-error" className="p-error">{getErrorMessage('emailAddress')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="userName">User Name <span className="p-error">*</span></label>
            <Controller name="userName" control={control} rules={ {required: 'Username is required',maxLength: { value: 100, message: 'Username cannot exceed 100 characters' },} }
              render={({ field: f }) => (
                <InputText id="userName" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('userName') ? 'p-invalid' : ''} aria-describedby="userName-error" />
              )}
            />
            {getErrorMessage('userName') && <small id="userName-error" className="p-error">{getErrorMessage('userName')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="encryptedPassword">Encrypted Password <span className="p-error">*</span></label>
            <Controller name="encryptedPassword" control={control} rules={ {required: 'Encryptedpassword is required',maxLength: { value: 255, message: 'Encryptedpassword cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="encryptedPassword" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('encryptedPassword') ? 'p-invalid' : ''} aria-describedby="encryptedPassword-error" />
              )}
            />
            {getErrorMessage('encryptedPassword') && <small id="encryptedPassword-error" className="p-error">{getErrorMessage('encryptedPassword')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="phoneNumber">Phone Number</label>
            <Controller name="phoneNumber" control={control} rules={ {maxLength: { value: 30, message: 'Phonenumber cannot exceed 30 characters' },} }
              render={({ field: f }) => (
                <InputText id="phoneNumber" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('phoneNumber') ? 'p-invalid' : ''} aria-describedby="phoneNumber-error" />
              )}
            />
            {getErrorMessage('phoneNumber') && <small id="phoneNumber-error" className="p-error">{getErrorMessage('phoneNumber')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="profilePhoto">Profile Photo</label>
            <Controller name="profilePhoto" control={control} rules={ {maxLength: { value: 255, message: 'Profilephoto cannot exceed 255 characters' },} }
              render={({ field: f }) => (
                <InputText id="profilePhoto" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('profilePhoto') ? 'p-invalid' : ''} aria-describedby="profilePhoto-error" />
              )}
            />
            {getErrorMessage('profilePhoto') && <small id="profilePhoto-error" className="p-error">{getErrorMessage('profilePhoto')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isActive">Is Active</label>
            <Controller name="isActive" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isActive" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isActive') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isActive') && <small id="isActive-error" className="p-error">{getErrorMessage('isActive')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isEntity">Is Entity</label>
            <Controller name="isEntity" control={control} rules={ {} }
              render={({ field: f }) => (
                <Checkbox id="isEntity" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isEntity') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isEntity') && <small id="isEntity-error" className="p-error">{getErrorMessage('isEntity')}</small>}
          </div>
        </div>
        <div className={getColClass('Checkbox')}>
          <div className="field p-mb-3">
            <label htmlFor="isPublic">Is Public <span className="p-error">*</span></label>
            <Controller name="isPublic" control={control} rules={ {required: 'Ispublic is required',} }
              render={({ field: f }) => (
                <Checkbox id="isPublic" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('isPublic') ? 'p-invalid' : ''} />
              )}
            />
            {getErrorMessage('isPublic') && <small id="isPublic-error" className="p-error">{getErrorMessage('isPublic')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.userId && (
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

export default UserForm;