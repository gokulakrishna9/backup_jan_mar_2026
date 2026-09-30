import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPostQuestion,
  getJobPostQuestionById,
  createJobPostQuestion as createJobPostQuestionApi,
  updateJobPostQuestion as updateJobPostQuestionApi,
  deleteJobPostQuestion as deleteJobPostQuestionApi,
} from '../../services/jobPostQuestionService';


export const fetchAllJobPostQuestion = createAsyncThunk(
  'jobPostQuestion/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPostQuestion(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPostQuestion = createAsyncThunk(
  'jobPostQuestion/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostQuestionById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPostQuestion = createAsyncThunk(
  'jobPostQuestion/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostQuestionApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPostQuestion = createAsyncThunk(
  'jobPostQuestion/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostQuestionApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPostQuestion = createAsyncThunk(
  'jobPostQuestion/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostQuestionApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostQuestionSlice = createSlice({
  name: 'jobPostQuestion',
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
      .addCase(fetchAllJobPostQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPostQuestion.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPostQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPostQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPostQuestion.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPostQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPostQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPostQuestion.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPostQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPostQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPostQuestion.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.questionId === action.payload.questionId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPostQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPostQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPostQuestion.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.questionId !== action.meta.arg);
      })
      .addCase(removeJobPostQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostQuestionSlice.actions;
export default jobPostQuestionSlice.reducer;