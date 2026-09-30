import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseInstructor,
  getCourseInstructorById,
  createCourseInstructor as createCourseInstructorApi,
  updateCourseInstructor as updateCourseInstructorApi,
  deleteCourseInstructor as deleteCourseInstructorApi,
} from '../../services/courseInstructorService';


export const fetchAllCourseInstructor = createAsyncThunk(
  'courseInstructor/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseInstructor(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseInstructor = createAsyncThunk(
  'courseInstructor/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseInstructorById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseInstructor = createAsyncThunk(
  'courseInstructor/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseInstructorApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseInstructor = createAsyncThunk(
  'courseInstructor/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseInstructorApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseInstructor = createAsyncThunk(
  'courseInstructor/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseInstructorApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseInstructorSlice = createSlice({
  name: 'courseInstructor',
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
      .addCase(fetchAllCourseInstructor.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseInstructor.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseInstructor.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseInstructor.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseInstructor.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseInstructor.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseInstructor.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseInstructor.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseInstructor.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseInstructor.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseInstructor.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.instructorLinkId === action.payload.instructorLinkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseInstructor.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseInstructor.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseInstructor.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.instructorLinkId !== action.meta.arg);
      })
      .addCase(removeCourseInstructor.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseInstructorSlice.actions;
export default courseInstructorSlice.reducer;