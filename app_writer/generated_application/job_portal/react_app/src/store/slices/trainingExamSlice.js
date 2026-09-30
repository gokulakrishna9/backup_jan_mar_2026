import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllTrainingExam,
  getTrainingExamById,
  createTrainingExam as createTrainingExamApi,
  updateTrainingExam as updateTrainingExamApi,
  deleteTrainingExam as deleteTrainingExamApi,
} from '../../services/trainingExamService';


export const fetchAllTrainingExam = createAsyncThunk(
  'trainingExam/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllTrainingExam(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdTrainingExam = createAsyncThunk(
  'trainingExam/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getTrainingExamById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createTrainingExam = createAsyncThunk(
  'trainingExam/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createTrainingExamApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateTrainingExam = createAsyncThunk(
  'trainingExam/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateTrainingExamApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeTrainingExam = createAsyncThunk(
  'trainingExam/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteTrainingExamApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const trainingExamSlice = createSlice({
  name: 'trainingExam',
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
      .addCase(fetchAllTrainingExam.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllTrainingExam.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllTrainingExam.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdTrainingExam.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdTrainingExam.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdTrainingExam.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createTrainingExam.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createTrainingExam.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createTrainingExam.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateTrainingExam.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateTrainingExam.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.trainingExamId === action.payload.trainingExamId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateTrainingExam.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeTrainingExam.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeTrainingExam.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.trainingExamId !== action.meta.arg);
      })
      .addCase(removeTrainingExam.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = trainingExamSlice.actions;
export default trainingExamSlice.reducer;