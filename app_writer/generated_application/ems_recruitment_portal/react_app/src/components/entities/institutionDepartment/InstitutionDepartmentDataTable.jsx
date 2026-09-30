import React, { useEffect, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Menu } from 'primereact/menu';
import { Dialog } from 'primereact/dialog';
import { Toast } from 'primereact/toast';
import { usePermissions } from '../../../hooks/usePermissions';
import { fetchAllInstitutionDepartment, removeInstitutionDepartment } from '../../../store/slices/institutionDepartmentSlice';
import logger from '../../../utils/logger';

const InstitutionDepartmentDataTable = ({ onRowSelect }) => {
  const dispatch = useDispatch();
  const toast = useRef(null);
  const { canView, canUpdate, canDelete } = usePermissions('/api/institutiondepartments');
  const { items, loading, currentPage, pageSize, totalCount } = useSelector((state) => state.institutionDepartment);
  const [deleteDialogVisible, setDeleteDialogVisible] = useState(false);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    dispatch(fetchAllInstitutionDepartment({ page: 0, size: pageSize }));
  }, [dispatch]);


  const onPage = (event) => {
    dispatch(fetchAllInstitutionDepartment({ page: event.page, size: event.rows }));
  };



  const confirmDelete = (id) => {
    setSelectedId(id);
    setDeleteDialogVisible(true);
  };

  const handleDelete = async () => {
    try {
      await dispatch(removeInstitutionDepartment(selectedId)).unwrap();
      toast.current?.show({ severity: 'success', summary: 'Deleted', life: 3000 });
    } catch (err) {
      logger.storeError('InstitutionDepartment delete', err);
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
      items.push({ label: 'Delete', icon: 'pi pi-trash', className: 'p-menuitem-danger', command: () => confirmDelete(rowData.departmentId) });
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
        <Column field="institutionId" header="Institution Id" sortable />
        <Column field="departmentName" header="Department Name" sortable />
        <Column field="description" header="Description" sortable />
        <Column field="headOfDepartmentUserId" header="Head Of Department User Id" sortable />
        <Column field="contactEmail" header="Contact Email" sortable />
        <Column field="contactPhone" header="Contact Phone" sortable />
        <Column field="isActive" header="Is Active" sortable />
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

export default InstitutionDepartmentDataTable;