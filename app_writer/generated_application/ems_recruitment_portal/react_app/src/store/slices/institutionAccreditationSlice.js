import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllInstitutionAccreditation,
  getInstitutionAccreditationById,
  createInstitutionAccreditation as createInstitutionAccreditationApi,
  updateInstitutionAccreditation as updateInstitutionAccreditationApi,
  deleteInstitutionAccreditation as deleteInstitutionAccreditationApi,
} from '../../services/institutionAccreditationService';


export const fetchAllInstitutionAccreditation = createAsyncThunk(
  'institutionAccreditation/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllInstitutionAccreditation(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdInstitutionAccreditation = createAsyncThunk(
  'institutionAccreditation/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getInstitutionAccreditationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createInstitutionAccreditation = createAsyncThunk(
  'institutionAccreditation/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createInstitutionAccreditationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateInstitutionAccreditation = createAsyncThunk(
  'institutionAccreditation/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateInstitutionAccreditationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeInstitutionAccreditation = createAsyncThunk(
  'institutionAccreditation/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteInstitutionAccreditationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const institutionAccreditationSlice = createSlice({
  name: 'institutionAccreditation',
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
      .addCase(fetchAllInstitutionAccreditation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllInstitutionAccreditation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllInstitutionAccreditation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdInstitutionAccreditation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdInstitutionAccreditation.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdInstitutionAccreditation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createInstitutionAccreditation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createInstitutionAccreditation.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createInstitutionAccreditation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateInstitutionAccreditation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateInstitutionAccreditation.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.accreditationId === action.payload.accreditationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateInstitutionAccreditation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeInstitutionAccreditation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeInstitutionAccreditation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.accreditationId !== action.meta.arg);
      })
      .addCase(removeInstitutionAccreditation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = institutionAccreditationSlice.actions;
export default institutionAccreditationSlice.reducer;