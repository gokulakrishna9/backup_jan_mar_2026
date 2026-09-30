import React, { useEffect, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Menu } from 'primereact/menu';
import { Dialog } from 'primereact/dialog';
import { Toast } from 'primereact/toast';
import { usePermissions } from '../../../hooks/usePermissions';
import { fetchAllUserWorkExperience, removeUserWorkExperience } from '../../../store/slices/userWorkExperienceSlice';
import logger from '../../../utils/logger';

const UserWorkExperienceDataTable = ({ onRowSelect }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canView, canUpdate, canDelete } = usePermissions('/api/user_work_experiences');
  const { items, loading, currentPage, pageSize, totalCount } = useSelector((state) => state.userWorkExperience);
  const [deleteDialogVisible, setDeleteDialogVisible] = useState(false);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    dispatch(fetchAllUserWorkExperience({ page: 0, size: pageSize }));
  }, [dispatch]);


  const onPage = (event) => {
    dispatch(fetchAllUserWorkExperience({ page: event.page, size: event.rows }));
  };



  const confirmDelete = (id) => {
    setSelectedId(id);
    setDeleteDialogVisible(true);
  };

  const handleDelete = async () => {
    try {
      await dispatch(removeUserWorkExperience(selectedId)).unwrap();
      toast.current?.show({ severity: 'success', summary: 'Deleted', life: 3000 });
    } catch (err) {
      logger.storeError('UserWorkExperience delete', err);
      toast.current?.show({ severity: 'error', summary: 'Error', detail: String(err), life: 5000 });
    }
    setDeleteDialogVisible(false);
    setSelectedId(null);
  };


  const actionBodyTemplate = (rowData) => {
    const menuRef = React.createRef();
    const items = [];
    if (canView) {
      items.push({ label: 'View', icon: 'pi pi-eye', command: () => onRowSelect && onRowSelect(rowData, 'view') });
    }
    if (canUpdate) {
      items.push({ label: 'Edit', icon: 'pi pi-pencil', command: () => onRowSelect && onRowSelect(rowData, 'edit') });
    }
    if (canDelete) {
      if (items.length > 0) items.push({ separator: true });
      items.push({ label: 'Delete', icon: 'pi pi-trash', className: 'p-menuitem-danger', command: () => confirmDelete(rowData.userWorkExperienceId) });
    }
    return (
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
        paginator
        rows={pageSize}
        totalRecords={totalCount}
        lazy
        first={currentPage * pageSize}
        onPage={onPage}
        sortMode="single"
        removableSort
        responsiveLayout="scroll"
      >
        <Column field="companyname" header="Companyname" sortable />
        <Column field="jobtitle" header="Jobtitle" sortable />
        <Column field="industry" header="Industry" sortable />
        <Column field="location" header="Location" sortable />
        <Column field="startdate" header="Startdate" sortable />
        <Column field="enddate" header="Enddate" sortable />
        <Column field="iscurrent" header="Iscurrent" sortable />
        <Column field="description" header="Description" sortable />
        <Column body={actionBodyTemplate} header="Actions" style={ { width: '10rem' } } />
      </DataTable>

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
    </div>
  );
};

export default UserWorkExperienceDataTable;