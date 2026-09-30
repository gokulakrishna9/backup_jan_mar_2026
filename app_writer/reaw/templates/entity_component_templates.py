"""Jinja2 templates for per-entity Form and DataTable components."""

ENTITY_FORM = """import React, { useState, useEffect, useRef } from 'react';
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
{% if hasCreateEndpoint %}import { create{{ entityNamePascal }} } from '../../../store/slices/{{ entityNameCamel }}Slice';{% endif %}
{% if hasUpdateEndpoint %}import { update{{ entityNamePascal }} } from '../../../store/slices/{{ entityNameCamel }}Slice';{% endif %}
{% if fields | selectattr('componentType', 'equalto', 'QuillEditor') | list %}import QuillEditorWidget from '../../widgets/QuillEditorWidget';
{% endif %}{% if fields | selectattr('componentType', 'equalto', 'MonacoEditor') | list %}import MonacoEditorWidget from '../../widgets/MonacoEditorWidget';
{% endif %}{% if fields | selectattr('componentType', 'equalto', 'MarkdownEditor') | list %}import MarkdownEditorWidget from '../../widgets/MarkdownEditorWidget';
{% endif %}{% if fields | selectattr('componentType', 'equalto', 'FileUpload') | list %}import FileUploadWidget from '../../widgets/FileUploadWidget';
{% endif %}import logger from '../../../utils/logger';
{% if singleRecordPerUser %}import apiClient from '../../../services/apiClient';
{% endif %}
const {{ entityNamePascal }}Form = ({ data{% if not singleRecordPerUser %}, mode = 'view'{% endif %}, onSave, onCancel, onNew, showForm = true{% if parentForeignKey %}, parentId{% endif %} }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canUpdate, canCreate, canGrantAccess } = usePermissions('{{ basePath }}');
{% if singleRecordPerUser %}  const [myRecord, setMyRecord] = useState(null);
  const [myRecordLoading, setMyRecordLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
{% else %}  const [editMode, setEditMode] = useState(mode === 'create');
{% endif %}
{% for field in fields %}{% if field.isRelationshipField %}  const [{{ field.fieldName }}Suggestions, set{{ field.fieldName | capitalize }}Suggestions] = useState([]);
{% endif %}{% endfor %}

  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
{% for field in fields %}      {{ field.fieldName }}: {{ "''" if field.componentType in ['InputText', 'InputTextarea'] else 'null' }},
{% endfor %}    },
  });

  useEffect(() => {
    if (data) {
      reset({ ...data });
    }
  }, [data, reset]);

{% if not singleRecordPerUser %}  useEffect(() => {
    setEditMode(mode === 'create' || mode === 'edit');
  }, [mode]);
{% endif %}
{% if singleRecordPerUser %}
  useEffect(() => {
    let cancelled = false;
    const fetchMyRecord = async () => {
      try {
        const response = await apiClient.get('{{ basePath }}/me');
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
{% endif %}

  const onSubmit = async (formData) => {
{% if parentForeignKey %}    const submitData = { ...formData, {{ parentForeignKey }}: parentId };
{% else %}    const submitData = { ...formData };
{% endif %}    try {
{% if singleRecordPerUser %}      const existingId = myRecord?.{{ pkField }};
      if (existingId) {
{% if hasUpdateEndpoint %}        await dispatch(update{{ entityNamePascal }}({ id: existingId, data: submitData })).unwrap();
{% endif %}      } else {
{% if hasCreateEndpoint %}        const result = await dispatch(create{{ entityNamePascal }}(submitData)).unwrap();
        setMyRecord(result);
{% endif %}      }
{% else %}      if (data?.{{ pkField }}) {
{% if hasUpdateEndpoint %}        await dispatch(update{{ entityNamePascal }}({ id: data.{{ pkField }}, data: submitData })).unwrap();
{% endif %}      } else {
{% if hasCreateEndpoint %}        await dispatch(create{{ entityNamePascal }}(submitData)).unwrap();
{% endif %}      }
{% endif %}      toast.current?.show({ severity: 'success', summary: 'Saved', life: 3000 });
      if (onSave) onSave();
{% if singleRecordPerUser %}      setEditMode(false);
{% endif %}    } catch (err) {
      logger.storeError('{{ entityNamePascal }} save', err);
      toast.current?.show({ severity: 'error', summary: 'Error', detail: String(err), life: 5000 });
    }
  };
{% for field in fields %}{% if field.isRelationshipField %}
  const search{{ field.fieldName | capitalize }} = async (event) => {
    try {
      const { default: apiClient } = await import('../../../services/apiClient');
      const response = await apiClient.get('/api/{{ field.relatedEntityName | lower }}', {
        params: { search: event.query, size: 10 },
      });
      set{{ field.fieldName | capitalize }}Suggestions(response.data.content || response.data || []);
    } catch (err) {
      set{{ field.fieldName | capitalize }}Suggestions([]);
    }
  };
{% endif %}{% endfor %}
  const isDisabled = !editMode;
{% if formLayout %}
  const colsLg = {{ formLayout.columnsLg }};
  const colsMd = {{ formLayout.columnsMd }};
  const colsSm = {{ formLayout.columnsSm }};
  const fullWidthTypes = [{{ formLayout.fullWidthComponentTypes | map('tojson') | join(', ') }}];
{% else %}
  const colsLg = 3;
  const colsMd = 2;
  const colsSm = 1;
  const fullWidthTypes = ['InputTextarea', 'QuillEditor', 'MonacoEditor', 'MarkdownEditor', 'FileUpload'];
{% endif %}

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
{% if singleRecordPerUser %}      {myRecordLoading ? (
        <div className="flex justify-content-center p-4"><i className="pi pi-spin pi-spinner" style={ { fontSize: '2rem' } } /></div>
      ) : (
      <>
{% endif %}      <div className="flex justify-content-end gap-2 mb-3">
{% if singleRecordPerUser %}{% if formButtons %}{% for btn in formButtons %}{% if btn.action == 'create' %}{% endif %}{% endfor %}{% endif %}
{% else %}{% if formButtons %}{% for btn in formButtons %}{% if btn.action == 'create' %}        {!editMode && canCreate && (
          <Button label="{{ btn.label }}" icon="{{ btn.icon }}" className="{{ btn.className }} p-button-sm" onClick={() => { reset({}); setEditMode(true); if (onNew) onNew(); }} />
        )}
{% endif %}{% endfor %}{% else %}        {!editMode && canCreate && (
          <Button label="New" icon="pi pi-plus" className="p-button-success p-button-sm" onClick={() => { reset({}); setEditMode(true); if (onNew) onNew(); }} />
        )}
{% endif %}{% endif %}      </div>
      {showForm && (
      <form onSubmit={handleSubmit(onSubmit)}>
      <div className="p-fluid">
      <div className="grid">
{% for field in fields %}{% if parentForeignKey and field.fieldName == parentForeignKey %}{% else %}        <div className={getColClass('{{ field.componentType }}')}>
          <div className="field p-mb-3">
            <label htmlFor="{{ field.fieldName }}">{{ field.fieldLabel }}{% if field.validation and field.validation.required %} <span className="p-error">*</span>{% endif %}</label>
            <Controller name="{{ field.fieldName }}" control={control} rules={ {{ '{' }}{% if field.validation %}{% if field.validation.required %}required: '{{ field.validation.requiredMessage or (field.fieldLabel + " is required") }}',{% endif %}{% if field.validation.minLength %}minLength: { value: {{ field.validation.minLength }}, message: '{{ field.validation.minLengthMessage or (field.fieldLabel + " must be at least " + field.validation.minLength|string + " characters") }}' },{% endif %}{% if field.validation.maxLength %}maxLength: { value: {{ field.validation.maxLength }}, message: '{{ field.validation.maxLengthMessage or (field.fieldLabel + " exceeds max length") }}' },{% endif %}{% if field.validation.email %}pattern: { value: /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/, message: '{{ field.validation.emailMessage or "Invalid email format" }}' },{% elif field.validation.pattern %}pattern: { value: /{{ field.validation.pattern }}/, message: '{{ field.validation.patternMessage or (field.fieldLabel + " format is invalid") }}' },{% endif %}{% endif %}{{ '}' }} }
              render={({ field: f }) => (
{% if field.componentType == 'InputText' %}                <InputText id="{{ field.fieldName }}" {...f} value={f.value || ''} disabled={isDisabled} className={getErrorMessage('{{ field.fieldName }}') ? 'p-invalid' : ''} aria-describedby="{{ field.fieldName }}-error" />
{% elif field.componentType == 'InputNumber' %}                <InputNumber id="{{ field.fieldName }}" value={f.value} onValueChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('{{ field.fieldName }}') ? 'p-invalid' : ''} aria-describedby="{{ field.fieldName }}-error" />
{% elif field.componentType == 'InputTextarea' %}                <InputTextarea id="{{ field.fieldName }}" {...f} value={f.value || ''} disabled={isDisabled} rows={3} className={getErrorMessage('{{ field.fieldName }}') ? 'p-invalid' : ''} aria-describedby="{{ field.fieldName }}-error" />
{% elif field.componentType == 'Calendar' %}                <Calendar id="{{ field.fieldName }}" value={f.value ? new Date(f.value) : null} onChange={(e) => f.onChange(e.value)} disabled={isDisabled}{% if field.props.mode == 'datetime' %} showTime{% endif %} className={getErrorMessage('{{ field.fieldName }}') ? 'p-invalid' : ''} aria-describedby="{{ field.fieldName }}-error" />
{% elif field.componentType == 'Checkbox' %}                <Checkbox id="{{ field.fieldName }}" checked={!!f.value} onChange={(e) => f.onChange(e.checked)} disabled={isDisabled} className={getErrorMessage('{{ field.fieldName }}') ? 'p-invalid' : ''} />
{% elif field.componentType == 'Dropdown' %}                <Dropdown id="{{ field.fieldName }}" value={f.value} options={ {{ field.props.options | default('[]') }} } onChange={(e) => f.onChange(e.value)} disabled={isDisabled} className={getErrorMessage('{{ field.fieldName }}') ? 'p-invalid' : ''} aria-describedby="{{ field.fieldName }}-error" />
{% elif field.componentType == 'AutoComplete' %}                <AutoComplete id="{{ field.fieldName }}" value={f.value} suggestions={ {{ field.fieldName }}Suggestions} completeMethod={search{{ field.fieldName | capitalize }}} field="{{ field.autocompleteDisplayField or 'name' }}" onChange={(e) => f.onChange(e.value)} disabled={isDisabled}{% if field.isMultiSelect %} multiple{% endif %} minLength={2} className={getErrorMessage('{{ field.fieldName }}') ? 'p-invalid' : ''} aria-describedby="{{ field.fieldName }}-error" />
{% elif field.componentType == 'QuillEditor' %}                <QuillEditorWidget id="{{ field.fieldName }}" value={f.value || ''} onChange={(val) => f.onChange(val)} disabled={isDisabled} entityType="{{ entityNamePascal }}" entityId={data?.{{ pkField }}} className={getErrorMessage('{{ field.fieldName }}') ? 'p-invalid' : ''} />
{% elif field.componentType == 'MonacoEditor' %}                <MonacoEditorWidget id="{{ field.fieldName }}" value={f.value || ''} onChange={(val) => f.onChange(val)} disabled={isDisabled} language="{{ field.props.language | default('javascript') }}" className={getErrorMessage('{{ field.fieldName }}') ? 'p-invalid' : ''} />
{% elif field.componentType == 'MarkdownEditor' %}                <MarkdownEditorWidget id="{{ field.fieldName }}" value={f.value || ''} onChange={(val) => f.onChange(val)} disabled={isDisabled} className={getErrorMessage('{{ field.fieldName }}') ? 'p-invalid' : ''} />
{% elif field.componentType == 'FileUpload' %}                <FileUploadWidget id="{{ field.fieldName }}" onChange={(meta) => f.onChange(meta)} disabled={isDisabled} entityType="{{ entityNamePascal }}" entityId={data?.{{ pkField }}} accept="{{ field.props.accept | default('') }}" />
{% endif %}              )}
            />
            {getErrorMessage('{{ field.fieldName }}') && <small id="{{ field.fieldName }}-error" className="p-error">{getErrorMessage('{{ field.fieldName }}')}</small>}
          </div>
        </div>
{% endif %}{% endfor %}      </div>
      </div>
      <div className="flex justify-content-end gap-2 mt-3">
{% if formButtons %}{% for btn in formButtons %}{% if btn.action == 'edit' %}        {!editMode && canUpdate && data?.{{ pkField }} && (
          <Button label="{{ btn.label }}" icon="{{ btn.icon }}" className="{{ btn.className }}" type="button" onClick={() => setEditMode(true)} />
        )}
{% elif btn.action == 'submit' %}        {editMode && (
          <Button label="{{ btn.label }}" icon="{{ btn.icon }}" className="{{ btn.className }}" type="submit" />
        )}
{% elif btn.action == 'cancel' %}        {editMode && (
          <Button label="{{ btn.label }}" icon="{{ btn.icon }}" className="{{ btn.className }}" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
        )}
{% elif btn.action == 'grantAccess' %}{% if isRootEntity %}        {canGrantAccess && data?.{{ pkField }} && (
          <Button label="{{ btn.label }}" icon="{{ btn.icon }}" className="{{ btn.className }}" type="button" onClick={() => { /* Grant access handler */ }} />
        )}
{% endif %}{% endif %}{% endfor %}{% else %}        {!editMode && canUpdate && data?.{{ pkField }} && (
          <Button label="Edit" icon="pi pi-pencil" className="p-button-info p-mr-2" type="button" onClick={() => setEditMode(true)} />
        )}
        {editMode && (
          <>
            <Button label="Save" icon="pi pi-check" className="p-button-success p-mr-2" type="submit" />
            <Button label="Cancel" icon="pi pi-times" className="p-button-secondary" type="button" onClick={() => { setEditMode(false); if (data) reset({ ...data }); if (onCancel) onCancel(); }} />
          </>
        )}
{% if isRootEntity %}        {canGrantAccess && data?.{{ pkField }} && (
          <Button label="Grant Access" icon="pi pi-lock-open" className="p-button-warning p-ml-2" type="button" onClick={() => { /* Grant access handler */ }} />
        )}
{% endif %}{% endif %}      </div>
      </form>
      )}
{% if singleRecordPerUser %}      </>
      )}
{% endif %}    </div>
  );
};

export default {{ entityNamePascal }}Form;
"""

ENTITY_DATATABLE = """import React, { useEffect, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Menu } from 'primereact/menu';
import { Dialog } from 'primereact/dialog';
import { Toast } from 'primereact/toast';
import { usePermissions } from '../../../hooks/usePermissions';
import { fetchAll{{ entityNamePascal }}{% if hasDeleteAction %}, remove{{ entityNamePascal }}{% endif %} } from '../../../store/slices/{{ entityNameCamel }}Slice';
import logger from '../../../utils/logger';

const {{ entityNamePascal }}DataTable = ({ onRowSelect }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canView, canUpdate, canDelete } = usePermissions('{{ basePath }}');
  const { items, loading{% if hasPagination %}, currentPage, pageSize, totalCount{% endif %} } = useSelector((state) => state.{{ entityNameCamel }});
  const [deleteDialogVisible, setDeleteDialogVisible] = useState(false);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    dispatch(fetchAll{{ entityNamePascal }}({% if hasPagination %}{ page: 0, size: {{ 'pageSize' }} }{% endif %}));
  }, [dispatch]);

{% if hasPagination %}
  const onPage = (event) => {
    dispatch(fetchAll{{ entityNamePascal }}({ page: event.page, size: event.rows }));
  };
{% endif %}

{% if hasDeleteAction %}
  const confirmDelete = (id) => {
    setSelectedId(id);
    setDeleteDialogVisible(true);
  };

  const handleDelete = async () => {
    try {
      await dispatch(remove{{ entityNamePascal }}(selectedId)).unwrap();
      toast.current?.show({ severity: 'success', summary: 'Deleted', life: 3000 });
    } catch (err) {
      logger.storeError('{{ entityNamePascal }} delete', err);
      toast.current?.show({ severity: 'error', summary: 'Error', detail: String(err), life: 5000 });
    }
    setDeleteDialogVisible(false);
    setSelectedId(null);
  };
{% endif %}

  const actionBodyTemplate = (rowData) => {
    const menuRef = React.createRef();
    const items = [];
{% if hasViewAction %}    if (canView) {
      items.push({ label: 'View', icon: 'pi pi-eye', command: () => onRowSelect && onRowSelect(rowData, 'view') });
    }
{% endif %}{% if hasUpdateAction %}    if (canUpdate) {
      items.push({ label: 'Edit', icon: 'pi pi-pencil', command: () => onRowSelect && onRowSelect(rowData, 'edit') });
    }
{% endif %}{% if hasDeleteAction %}    if (canDelete) {
      if (items.length > 0) items.push({ separator: true });
      items.push({ label: 'Delete', icon: 'pi pi-trash', className: 'p-menuitem-danger', command: () => confirmDelete(rowData.{{ pkField }}) });
    }
{% endif %}    return (
      <>
        <Menu model={items} popup ref={menuRef} popupAlignment="right" />
        <Button icon="pi pi-ellipsis-v" className="p-button-text p-button-sm p-button-rounded" onClick={(e) => menuRef.current.toggle(e)} />
      </>
    );
  };

  return (
    <div>
      <Toast ref={toast} />
      <DataTable
        value={items}
        loading={loading}
{% if hasPagination %}        paginator
        rows={pageSize}
        totalRecords={totalCount}
        lazy
        first={currentPage * pageSize}
        onPage={onPage}
{% endif %}{% if hasSorting %}        sortMode="single"
        removableSort
{% endif %}        responsiveLayout="scroll"
      >
{% for col in columns %}{% if col.fieldWidget == 'richText' %}        <Column field="{{ col.fieldName }}" header="{{ col.header }}" body={(rowData) => { const val = rowData.{{ col.fieldName }} || ''; const text = val.replace(/<[^>]*>/g, ''); return text.length > 100 ? text.substring(0, 100) + '...' : text; }} />
{% elif col.fieldWidget in ['codeEditor', 'markdown', 'json'] %}        <Column field="{{ col.fieldName }}" header="{{ col.header }}" body={(rowData) => { const val = String(rowData.{{ col.fieldName }} || ''); return <span style={ { fontFamily: 'monospace', fontSize: '0.85em' } }>{val.length > 100 ? val.substring(0, 100) + '...' : val}</span>; }} />
{% else %}        <Column field="{{ col.fieldName }}" header="{{ col.header }}"{% if col.sortable %} sortable{% endif %} />
{% endif %}{% endfor %}        <Column body={actionBodyTemplate} header="Actions" style={ { width: '10rem' } } />
      </DataTable>
{% if hasDeleteAction %}
      <Dialog
        visible={deleteDialogVisible}
        onHide={() => setDeleteDialogVisible(false)}
        header="Confirm Delete"
        footer={
          <div>
            <Button label="Cancel" icon="pi pi-times" className="p-button-text" onClick={() => setDeleteDialogVisible(false)} />
            <Button label="Delete" icon="pi pi-trash" className="p-button-danger" onClick={handleDelete} />
          </div>
        }
      >
        <p>Are you sure you want to delete this record?</p>
      </Dialog>
{% endif %}    </div>
  );
};

export default {{ entityNamePascal }}DataTable;
"""
