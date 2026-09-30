import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCompany,
  getCompanyById,
  createCompany as createCompanyApi,
  updateCompany as updateCompanyApi,
  deleteCompany as deleteCompanyApi,
} from '../../services/companyService';


export const fetchAllCompany = createAsyncThunk(
  'company/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCompany(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCompany = createAsyncThunk(
  'company/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCompanyById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCompany = createAsyncThunk(
  'company/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCompanyApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCompany = createAsyncThunk(
  'company/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCompanyApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCompany = createAsyncThunk(
  'company/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCompanyApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const companySlice = createSlice({
  name: 'company',
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
      .addCase(fetchAllCompany.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCompany.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCompany.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCompany.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCompany.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCompany.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCompany.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCompany.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCompany.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCompany.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCompany.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.companyId === action.payload.companyId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCompany.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCompany.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCompany.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.companyId !== action.meta.arg);
      })
      .addCase(removeCompany.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = companySlice.actions;
export default companySlice.reducer;