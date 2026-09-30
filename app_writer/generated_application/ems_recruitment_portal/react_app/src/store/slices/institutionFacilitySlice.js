import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllInstitutionFacility,
  getInstitutionFacilityById,
  createInstitutionFacility as createInstitutionFacilityApi,
  updateInstitutionFacility as updateInstitutionFacilityApi,
  deleteInstitutionFacility as deleteInstitutionFacilityApi,
} from '../../services/institutionFacilityService';


export const fetchAllInstitutionFacility = createAsyncThunk(
  'institutionFacility/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllInstitutionFacility(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdInstitutionFacility = createAsyncThunk(
  'institutionFacility/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getInstitutionFacilityById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createInstitutionFacility = createAsyncThunk(
  'institutionFacility/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createInstitutionFacilityApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateInstitutionFacility = createAsyncThunk(
  'institutionFacility/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateInstitutionFacilityApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeInstitutionFacility = createAsyncThunk(
  'institutionFacility/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteInstitutionFacilityApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const institutionFacilitySlice = createSlice({
  name: 'institutionFacility',
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
      .addCase(fetchAllInstitutionFacility.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllInstitutionFacility.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllInstitutionFacility.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdInstitutionFacility.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdInstitutionFacility.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdInstitutionFacility.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createInstitutionFacility.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createInstitutionFacility.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createInstitutionFacility.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateInstitutionFacility.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateInstitutionFacility.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.facilityId === action.payload.facilityId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateInstitutionFacility.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeInstitutionFacility.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeInstitutionFacility.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.facilityId !== action.meta.arg);
      })
      .addCase(removeInstitutionFacility.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = institutionFacilitySlice.actions;
export default institutionFacilitySlice.reducer;