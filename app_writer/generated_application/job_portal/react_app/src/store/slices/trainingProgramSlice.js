import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllTrainingProgram,
  getTrainingProgramById,
  createTrainingProgram as createTrainingProgramApi,
  updateTrainingProgram as updateTrainingProgramApi,
  deleteTrainingProgram as deleteTrainingProgramApi,
} from '../../services/trainingProgramService';


export const fetchAllTrainingProgram = createAsyncThunk(
  'trainingProgram/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllTrainingProgram(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdTrainingProgram = createAsyncThunk(
  'trainingProgram/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getTrainingProgramById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createTrainingProgram = createAsyncThunk(
  'trainingProgram/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createTrainingProgramApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateTrainingProgram = createAsyncThunk(
  'trainingProgram/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateTrainingProgramApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeTrainingProgram = createAsyncThunk(
  'trainingProgram/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteTrainingProgramApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const trainingProgramSlice = createSlice({
  name: 'trainingProgram',
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
      .addCase(fetchAllTrainingProgram.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllTrainingProgram.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllTrainingProgram.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdTrainingProgram.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdTrainingProgram.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdTrainingProgram.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createTrainingProgram.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createTrainingProgram.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createTrainingProgram.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateTrainingProgram.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateTrainingProgram.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.trainingProgramId === action.payload.trainingProgramId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateTrainingProgram.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeTrainingProgram.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeTrainingProgram.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.trainingProgramId !== action.meta.arg);
      })
      .addCase(removeTrainingProgram.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = trainingProgramSlice.actions;
export default trainingProgramSlice.reducer;