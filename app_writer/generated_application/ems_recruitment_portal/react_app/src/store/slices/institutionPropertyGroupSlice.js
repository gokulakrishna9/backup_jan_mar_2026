import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllInstitutionPropertyGroup,
  getInstitutionPropertyGroupById,
  createInstitutionPropertyGroup as createInstitutionPropertyGroupApi,
  updateInstitutionPropertyGroup as updateInstitutionPropertyGroupApi,
  deleteInstitutionPropertyGroup as deleteInstitutionPropertyGroupApi,
} from '../../services/institutionPropertyGroupService';


export const fetchAllInstitutionPropertyGroup = createAsyncThunk(
  'institutionPropertyGroup/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllInstitutionPropertyGroup(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdInstitutionPropertyGroup = createAsyncThunk(
  'institutionPropertyGroup/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getInstitutionPropertyGroupById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createInstitutionPropertyGroup = createAsyncThunk(
  'institutionPropertyGroup/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createInstitutionPropertyGroupApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateInstitutionPropertyGroup = createAsyncThunk(
  'institutionPropertyGroup/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateInstitutionPropertyGroupApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeInstitutionPropertyGroup = createAsyncThunk(
  'institutionPropertyGroup/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteInstitutionPropertyGroupApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const institutionPropertyGroupSlice = createSlice({
  name: 'institutionPropertyGroup',
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
      .addCase(fetchAllInstitutionPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllInstitutionPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllInstitutionPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdInstitutionPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdInstitutionPropertyGroup.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdInstitutionPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createInstitutionPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createInstitutionPropertyGroup.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createInstitutionPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateInstitutionPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateInstitutionPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.groupId === action.payload.groupId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateInstitutionPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeInstitutionPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeInstitutionPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.groupId !== action.meta.arg);
      })
      .addCase(removeInstitutionPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = institutionPropertyGroupSlice.actions;
export default institutionPropertyGroupSlice.reducer;