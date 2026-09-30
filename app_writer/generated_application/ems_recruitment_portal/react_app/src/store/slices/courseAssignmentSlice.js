import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseAssignment,
  getCourseAssignmentById,
  createCourseAssignment as createCourseAssignmentApi,
  updateCourseAssignment as updateCourseAssignmentApi,
  deleteCourseAssignment as deleteCourseAssignmentApi,
} from '../../services/courseAssignmentService';


export const fetchAllCourseAssignment = createAsyncThunk(
  'courseAssignment/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseAssignment(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseAssignment = createAsyncThunk(
  'courseAssignment/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseAssignmentById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseAssignment = createAsyncThunk(
  'courseAssignment/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseAssignmentApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseAssignment = createAsyncThunk(
  'courseAssignment/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseAssignmentApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseAssignment = createAsyncThunk(
  'courseAssignment/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseAssignmentApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseAssignmentSlice = createSlice({
  name: 'courseAssignment',
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
      .addCase(fetchAllCourseAssignment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseAssignment.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseAssignment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseAssignment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseAssignment.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseAssignment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseAssignment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseAssignment.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseAssignment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseAssignment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseAssignment.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.assignmentId === action.payload.assignmentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseAssignment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseAssignment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseAssignment.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.assignmentId !== action.meta.arg);
      })
      .addCase(removeCourseAssignment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseAssignmentSlice.actions;
export default courseAssignmentSlice.reducer;