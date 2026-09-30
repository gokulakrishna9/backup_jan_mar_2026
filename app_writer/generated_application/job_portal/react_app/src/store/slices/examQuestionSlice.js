import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllExamQuestion,
  getExamQuestionById,
  createExamQuestion as createExamQuestionApi,
  updateExamQuestion as updateExamQuestionApi,
  deleteExamQuestion as deleteExamQuestionApi,
} from '../../services/examQuestionService';


export const fetchAllExamQuestion = createAsyncThunk(
  'examQuestion/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllExamQuestion(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdExamQuestion = createAsyncThunk(
  'examQuestion/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getExamQuestionById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createExamQuestion = createAsyncThunk(
  'examQuestion/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createExamQuestionApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateExamQuestion = createAsyncThunk(
  'examQuestion/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateExamQuestionApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeExamQuestion = createAsyncThunk(
  'examQuestion/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteExamQuestionApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const examQuestionSlice = createSlice({
  name: 'examQuestion',
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
      .addCase(fetchAllExamQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllExamQuestion.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllExamQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdExamQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdExamQuestion.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdExamQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createExamQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createExamQuestion.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createExamQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateExamQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateExamQuestion.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.examQuestionId === action.payload.examQuestionId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateExamQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeExamQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeExamQuestion.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.examQuestionId !== action.meta.arg);
      })
      .addCase(removeExamQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = examQuestionSlice.actions;
export default examQuestionSlice.reducer;