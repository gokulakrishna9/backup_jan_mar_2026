import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllInstitutionFile,
  getInstitutionFileById,
  createInstitutionFile as createInstitutionFileApi,
  updateInstitutionFile as updateInstitutionFileApi,
  deleteInstitutionFile as deleteInstitutionFileApi,
} from '../../services/institutionFileService';


export const fetchAllInstitutionFile = createAsyncThunk(
  'institutionFile/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllInstitutionFile(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdInstitutionFile = createAsyncThunk(
  'institutionFile/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getInstitutionFileById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createInstitutionFile = createAsyncThunk(
  'institutionFile/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createInstitutionFileApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateInstitutionFile = createAsyncThunk(
  'institutionFile/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateInstitutionFileApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeInstitutionFile = createAsyncThunk(
  'institutionFile/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteInstitutionFileApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const institutionFileSlice = createSlice({
  name: 'institutionFile',
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
      .addCase(fetchAllInstitutionFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllInstitutionFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllInstitutionFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdInstitutionFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdInstitutionFile.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdInstitutionFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createInstitutionFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createInstitutionFile.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createInstitutionFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateInstitutionFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateInstitutionFile.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.fileId === action.payload.fileId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateInstitutionFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeInstitutionFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeInstitutionFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.fileId !== action.meta.arg);
      })
      .addCase(removeInstitutionFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = institutionFileSlice.actions;
export default institutionFileSlice.reducer;