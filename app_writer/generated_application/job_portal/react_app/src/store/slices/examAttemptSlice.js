import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllExamAttempt,
  getExamAttemptById,
  createExamAttempt as createExamAttemptApi,
  updateExamAttempt as updateExamAttemptApi,
  deleteExamAttempt as deleteExamAttemptApi,
} from '../../services/examAttemptService';


export const fetchAllExamAttempt = createAsyncThunk(
  'examAttempt/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllExamAttempt(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdExamAttempt = createAsyncThunk(
  'examAttempt/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getExamAttemptById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createExamAttempt = createAsyncThunk(
  'examAttempt/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createExamAttemptApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateExamAttempt = createAsyncThunk(
  'examAttempt/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateExamAttemptApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeExamAttempt = createAsyncThunk(
  'examAttempt/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteExamAttemptApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const examAttemptSlice = createSlice({
  name: 'examAttempt',
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
      .addCase(fetchAllExamAttempt.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllExamAttempt.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllExamAttempt.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdExamAttempt.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdExamAttempt.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdExamAttempt.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createExamAttempt.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createExamAttempt.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createExamAttempt.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateExamAttempt.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateExamAttempt.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.examAttemptId === action.payload.examAttemptId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateExamAttempt.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeExamAttempt.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeExamAttempt.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.examAttemptId !== action.meta.arg);
      })
      .addCase(removeExamAttempt.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = examAttemptSlice.actions;
export default examAttemptSlice.reducer;