import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllModuleProgress,
  getModuleProgressById,
  createModuleProgress as createModuleProgressApi,
  updateModuleProgress as updateModuleProgressApi,
  deleteModuleProgress as deleteModuleProgressApi,
} from '../../services/moduleProgressService';


export const fetchAllModuleProgress = createAsyncThunk(
  'moduleProgress/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllModuleProgress(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdModuleProgress = createAsyncThunk(
  'moduleProgress/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getModuleProgressById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createModuleProgress = createAsyncThunk(
  'moduleProgress/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createModuleProgressApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateModuleProgress = createAsyncThunk(
  'moduleProgress/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateModuleProgressApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeModuleProgress = createAsyncThunk(
  'moduleProgress/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteModuleProgressApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const moduleProgressSlice = createSlice({
  name: 'moduleProgress',
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
      .addCase(fetchAllModuleProgress.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllModuleProgress.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllModuleProgress.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdModuleProgress.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdModuleProgress.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdModuleProgress.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createModuleProgress.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createModuleProgress.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createModuleProgress.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateModuleProgress.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateModuleProgress.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.moduleProgressId === action.payload.moduleProgressId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateModuleProgress.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeModuleProgress.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeModuleProgress.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.moduleProgressId !== action.meta.arg);
      })
      .addCase(removeModuleProgress.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = moduleProgressSlice.actions;
export default moduleProgressSlice.reducer;