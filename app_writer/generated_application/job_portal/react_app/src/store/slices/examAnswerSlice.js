import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllExamAnswer,
  getExamAnswerById,
  createExamAnswer as createExamAnswerApi,
  updateExamAnswer as updateExamAnswerApi,
  deleteExamAnswer as deleteExamAnswerApi,
} from '../../services/examAnswerService';


export const fetchAllExamAnswer = createAsyncThunk(
  'examAnswer/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllExamAnswer(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdExamAnswer = createAsyncThunk(
  'examAnswer/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getExamAnswerById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createExamAnswer = createAsyncThunk(
  'examAnswer/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createExamAnswerApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateExamAnswer = createAsyncThunk(
  'examAnswer/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateExamAnswerApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeExamAnswer = createAsyncThunk(
  'examAnswer/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteExamAnswerApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const examAnswerSlice = createSlice({
  name: 'examAnswer',
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
      .addCase(fetchAllExamAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllExamAnswer.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllExamAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdExamAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdExamAnswer.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdExamAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createExamAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createExamAnswer.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createExamAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateExamAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateExamAnswer.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.examAnswerId === action.payload.examAnswerId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateExamAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeExamAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeExamAnswer.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.examAnswerId !== action.meta.arg);
      })
      .addCase(removeExamAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = examAnswerSlice.actions;
export default examAnswerSlice.reducer;