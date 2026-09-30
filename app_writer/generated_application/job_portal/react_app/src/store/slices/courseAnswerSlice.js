import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseAnswer,
  getCourseAnswerById,
  createCourseAnswer as createCourseAnswerApi,
  updateCourseAnswer as updateCourseAnswerApi,
  deleteCourseAnswer as deleteCourseAnswerApi,
} from '../../services/courseAnswerService';


export const fetchAllCourseAnswer = createAsyncThunk(
  'courseAnswer/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseAnswer(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseAnswer = createAsyncThunk(
  'courseAnswer/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseAnswerById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseAnswer = createAsyncThunk(
  'courseAnswer/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseAnswerApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseAnswer = createAsyncThunk(
  'courseAnswer/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseAnswerApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseAnswer = createAsyncThunk(
  'courseAnswer/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseAnswerApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseAnswerSlice = createSlice({
  name: 'courseAnswer',
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
      .addCase(fetchAllCourseAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseAnswer.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseAnswer.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseAnswer.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseAnswer.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.courseAnswerId === action.payload.courseAnswerId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseAnswer.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseAnswer.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.courseAnswerId !== action.meta.arg);
      })
      .addCase(removeCourseAnswer.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseAnswerSlice.actions;
export default courseAnswerSlice.reducer;