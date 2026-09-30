import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseLesson,
  getCourseLessonById,
  createCourseLesson as createCourseLessonApi,
  updateCourseLesson as updateCourseLessonApi,
  deleteCourseLesson as deleteCourseLessonApi,
} from '../../services/courseLessonService';


export const fetchAllCourseLesson = createAsyncThunk(
  'courseLesson/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseLesson(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseLesson = createAsyncThunk(
  'courseLesson/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseLessonById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseLesson = createAsyncThunk(
  'courseLesson/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseLessonApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseLesson = createAsyncThunk(
  'courseLesson/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseLessonApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseLesson = createAsyncThunk(
  'courseLesson/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseLessonApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseLessonSlice = createSlice({
  name: 'courseLesson',
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
      .addCase(fetchAllCourseLesson.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseLesson.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseLesson.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseLesson.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseLesson.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseLesson.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseLesson.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseLesson.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseLesson.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseLesson.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseLesson.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.lessonId === action.payload.lessonId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseLesson.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseLesson.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseLesson.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.lessonId !== action.meta.arg);
      })
      .addCase(removeCourseLesson.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseLessonSlice.actions;
export default courseLessonSlice.reducer;