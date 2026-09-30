import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllInstitutionDepartment,
  getInstitutionDepartmentById,
  createInstitutionDepartment as createInstitutionDepartmentApi,
  updateInstitutionDepartment as updateInstitutionDepartmentApi,
  deleteInstitutionDepartment as deleteInstitutionDepartmentApi,
} from '../../services/institutionDepartmentService';


export const fetchAllInstitutionDepartment = createAsyncThunk(
  'institutionDepartment/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllInstitutionDepartment(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdInstitutionDepartment = createAsyncThunk(
  'institutionDepartment/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getInstitutionDepartmentById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createInstitutionDepartment = createAsyncThunk(
  'institutionDepartment/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createInstitutionDepartmentApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateInstitutionDepartment = createAsyncThunk(
  'institutionDepartment/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateInstitutionDepartmentApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeInstitutionDepartment = createAsyncThunk(
  'institutionDepartment/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteInstitutionDepartmentApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const institutionDepartmentSlice = createSlice({
  name: 'institutionDepartment',
  initialState: {
    items: [],
    selectedItem: null,
    loading: false,
    error: null,
    currentPage: 0,
    pageSize: 20,
    totalCount: 0,
  },
  reducers: {
    clearError: (state) => { state.error = null; },
    clearSelectedItem: (state) => { state.selectedItem = null; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAllInstitutionDepartment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllInstitutionDepartment.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllInstitutionDepartment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdInstitutionDepartment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdInstitutionDepartment.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdInstitutionDepartment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createInstitutionDepartment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createInstitutionDepartment.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createInstitutionDepartment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateInstitutionDepartment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateInstitutionDepartment.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.departmentId === action.payload.departmentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateInstitutionDepartment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeInstitutionDepartment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeInstitutionDepartment.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.departmentId !== action.meta.arg);
      })
      .addCase(removeInstitutionDepartment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = institutionDepartmentSlice.actions;
export default institutionDepartmentSlice.reducer;