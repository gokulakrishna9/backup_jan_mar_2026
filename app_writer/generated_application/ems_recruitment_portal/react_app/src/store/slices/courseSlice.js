import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourse,
  getCourseById,
  createCourse as createCourseApi,
  updateCourse as updateCourseApi,
  deleteCourse as deleteCourseApi,
} from '../../services/courseService';


export const fetchAllCourse = createAsyncThunk(
  'course/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourse(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourse = createAsyncThunk(
  'course/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourse = createAsyncThunk(
  'course/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourse = createAsyncThunk(
  'course/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourse = createAsyncThunk(
  'course/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseSlice = createSlice({
  name: 'course',
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
      .addCase(fetchAllCourse.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourse.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourse.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourse.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourse.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourse.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourse.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourse.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourse.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourse.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourse.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.courseId === action.payload.courseId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourse.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourse.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourse.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.courseId !== action.meta.arg);
      })
      .addCase(removeCourse.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseSlice.actions;
export default courseSlice.reducer;