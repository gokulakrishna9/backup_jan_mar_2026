import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllTrainingModule,
  getTrainingModuleById,
  createTrainingModule as createTrainingModuleApi,
  updateTrainingModule as updateTrainingModuleApi,
  deleteTrainingModule as deleteTrainingModuleApi,
} from '../../services/trainingModuleService';


export const fetchAllTrainingModule = createAsyncThunk(
  'trainingModule/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllTrainingModule(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdTrainingModule = createAsyncThunk(
  'trainingModule/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getTrainingModuleById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createTrainingModule = createAsyncThunk(
  'trainingModule/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createTrainingModuleApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateTrainingModule = createAsyncThunk(
  'trainingModule/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateTrainingModuleApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeTrainingModule = createAsyncThunk(
  'trainingModule/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteTrainingModuleApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const trainingModuleSlice = createSlice({
  name: 'trainingModule',
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
      .addCase(fetchAllTrainingModule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllTrainingModule.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllTrainingModule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdTrainingModule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdTrainingModule.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdTrainingModule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createTrainingModule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createTrainingModule.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createTrainingModule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateTrainingModule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateTrainingModule.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.trainingModuleId === action.payload.trainingModuleId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateTrainingModule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeTrainingModule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeTrainingModule.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.trainingModuleId !== action.meta.arg);
      })
      .addCase(removeTrainingModule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = trainingModuleSlice.actions;
export default trainingModuleSlice.reducer;