import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllTrainingEnrollment,
  getTrainingEnrollmentById,
  createTrainingEnrollment as createTrainingEnrollmentApi,
  updateTrainingEnrollment as updateTrainingEnrollmentApi,
  deleteTrainingEnrollment as deleteTrainingEnrollmentApi,
} from '../../services/trainingEnrollmentService';


export const fetchAllTrainingEnrollment = createAsyncThunk(
  'trainingEnrollment/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllTrainingEnrollment(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdTrainingEnrollment = createAsyncThunk(
  'trainingEnrollment/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getTrainingEnrollmentById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createTrainingEnrollment = createAsyncThunk(
  'trainingEnrollment/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createTrainingEnrollmentApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateTrainingEnrollment = createAsyncThunk(
  'trainingEnrollment/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateTrainingEnrollmentApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeTrainingEnrollment = createAsyncThunk(
  'trainingEnrollment/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteTrainingEnrollmentApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const trainingEnrollmentSlice = createSlice({
  name: 'trainingEnrollment',
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
      .addCase(fetchAllTrainingEnrollment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllTrainingEnrollment.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllTrainingEnrollment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdTrainingEnrollment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdTrainingEnrollment.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdTrainingEnrollment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createTrainingEnrollment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createTrainingEnrollment.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createTrainingEnrollment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateTrainingEnrollment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateTrainingEnrollment.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.trainingEnrollmentId === action.payload.trainingEnrollmentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateTrainingEnrollment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeTrainingEnrollment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeTrainingEnrollment.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.trainingEnrollmentId !== action.meta.arg);
      })
      .addCase(removeTrainingEnrollment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = trainingEnrollmentSlice.actions;
export default trainingEnrollmentSlice.reducer;