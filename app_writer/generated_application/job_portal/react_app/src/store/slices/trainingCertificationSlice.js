import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllTrainingCertification,
  getTrainingCertificationById,
  createTrainingCertification as createTrainingCertificationApi,
  updateTrainingCertification as updateTrainingCertificationApi,
  deleteTrainingCertification as deleteTrainingCertificationApi,
} from '../../services/trainingCertificationService';


export const fetchAllTrainingCertification = createAsyncThunk(
  'trainingCertification/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllTrainingCertification(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdTrainingCertification = createAsyncThunk(
  'trainingCertification/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getTrainingCertificationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createTrainingCertification = createAsyncThunk(
  'trainingCertification/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createTrainingCertificationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateTrainingCertification = createAsyncThunk(
  'trainingCertification/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateTrainingCertificationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeTrainingCertification = createAsyncThunk(
  'trainingCertification/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteTrainingCertificationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const trainingCertificationSlice = createSlice({
  name: 'trainingCertification',
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
      .addCase(fetchAllTrainingCertification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllTrainingCertification.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllTrainingCertification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdTrainingCertification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdTrainingCertification.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdTrainingCertification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createTrainingCertification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createTrainingCertification.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createTrainingCertification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateTrainingCertification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateTrainingCertification.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.trainingCertificationId === action.payload.trainingCertificationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateTrainingCertification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeTrainingCertification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeTrainingCertification.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.trainingCertificationId !== action.meta.arg);
      })
      .addCase(removeTrainingCertification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = trainingCertificationSlice.actions;
export default trainingCertificationSlice.reducer;