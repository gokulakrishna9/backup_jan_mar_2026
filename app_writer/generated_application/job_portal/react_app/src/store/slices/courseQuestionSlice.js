import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseQuestion,
  getCourseQuestionById,
  createCourseQuestion as createCourseQuestionApi,
  updateCourseQuestion as updateCourseQuestionApi,
  deleteCourseQuestion as deleteCourseQuestionApi,
} from '../../services/courseQuestionService';


export const fetchAllCourseQuestion = createAsyncThunk(
  'courseQuestion/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseQuestion(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseQuestion = createAsyncThunk(
  'courseQuestion/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseQuestionById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseQuestion = createAsyncThunk(
  'courseQuestion/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseQuestionApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseQuestion = createAsyncThunk(
  'courseQuestion/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseQuestionApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseQuestion = createAsyncThunk(
  'courseQuestion/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseQuestionApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseQuestionSlice = createSlice({
  name: 'courseQuestion',
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
      .addCase(fetchAllCourseQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseQuestion.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseQuestion.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseQuestion.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseQuestion.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.courseQuestionId === action.payload.courseQuestionId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseQuestion.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseQuestion.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.courseQuestionId !== action.meta.arg);
      })
      .addCase(removeCourseQuestion.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseQuestionSlice.actions;
export default courseQuestionSlice.reducer;