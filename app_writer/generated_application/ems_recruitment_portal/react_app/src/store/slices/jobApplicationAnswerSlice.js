import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobApplicationAnswer,
  getJobApplicationAnswerById,
  createJobApplicationAnswer as createJobApplicationAnswerApi,
  updateJobApplicationAnswer as updateJobApplicationAnswerApi,
  deleteJobApplicationAnswer as deleteJobApplicationAnswerApi,
} from '../../services/jobApplicationAnswerService';


export const fetchAllJobApplicationAnswer = createAsyncThunk(
  'jobApplicationAnswer/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobApplicationAnswer(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobApplicationAnswer = createAsyncThunk(
  'jobApplicationAnswer/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobApplicationAnswerById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobApplicationAnswer = createAsyncThunk(
  'jobApplicationAnswer/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobApplicationAnswerApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobApplicationAnswer = createAsyncThunk(
  'jobApplicationAnswer/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobApplicationAnswerApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobApplicationAnswer = createAsyncThunk(
  'jobApplicationAnswer/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobApplicationAnswerApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobApplicationAnswerSlice = createSlice({
  name: 'jobApplicationAnswer',
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
      .addCase(fetchAllJobApplicationAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobApplicationAnswer.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobApplicationAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobApplicationAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobApplicationAnswer.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobApplicationAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobApplicationAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobApplicationAnswer.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobApplicationAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobApplicationAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobApplicationAnswer.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.answerId === action.payload.answerId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobApplicationAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobApplicationAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobApplicationAnswer.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.answerId !== action.meta.arg);
      })
      .addCase(removeJobApplicationAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobApplicationAnswerSlice.actions;
export default jobApplicationAnswerSlice.reducer;