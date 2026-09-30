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
import { createTrainerProfile } from '../../../store/slices/trainerProfileSlice';
import { updateTrainerProfile } from '../../../store/slices/trainerProfileSlice';
import logger from '../../../utils/logger';
import apiClient from '../../../services/apiClient';

const TrainerProfileForm = ({ data, onSave, onCancel, onNew, showForm = true, parentId }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('/api/trainer_profiles');
  const [myRecord, setMyRecord] = useState(null);
  const [myRecordLoading, setMyRecordLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);



  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      specialization: '',
      certifications: '',
      hourlyrate: null,
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
        const response = await apiClient.get('/api/trainer_profiles/me');
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
      const existingId = myRecord?.trainerProfileId;
      if (existingId) {
        await dispatch(updateTrainerProfile({ id: existingId, data: submitData })).unwrap();
      } else {
        const result = await dispatch(createTrainerProfile(submitData)).unwrap();
        setMyRecord(result);
      }
      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
      setEditMode(false);
    } catch (err) {
      logger.storeError('TrainerProfile save', err);
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
            <label htmlFor="specialization">Specialization</label>
            <Controller name="specialization" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="specialization" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('specialization') ? 'p-invalid' : ''} aria-describedby="specialization-error" />
              )}
            />
            {getErrorMessage('specialization') && <small id="specialization-error" className="p-error">{getErrorMessage('specialization')}</small>}
          </div>
        </div>
        <div className={getColClass('InputText')}>
          <div className="field p-mb-3">
            <label htmlFor="certifications">Certifications</label>
            <Controller name="certifications" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputText id="certifications" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('certifications') ? 'p-invalid' : ''} aria-describedby="certifications-error" />
              )}
            />
            {getErrorMessage('certifications') && <small id="certifications-error" className="p-error">{getErrorMessage('certifications')}</small>}
          </div>
        </div>
        <div className={getColClass('InputNumber')}>
          <div className="field p-mb-3">
            <label htmlFor="hourlyrate">Hourlyrate</label>
            <Controller name="hourlyrate" control={control} rules={ {} }
              render={({ field: f }) => (
                <InputNumber id="hourlyrate" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('hourlyrate') ? 'p-invalid' : ''} aria-describedby="hourlyrate-error" />
              )}
            />
            {getErrorMessage('hourlyrate') && <small id="hourlyrate-error" className="p-error">{getErrorMessage('hourlyrate')}</small>}
          </div>
        </div>
      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
        {!editMode && canUpdate && data?.trainerProfileId && (
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

export default TrainerProfileForm;