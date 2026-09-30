import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCoursePrerequisite,
  getCoursePrerequisiteById,
  createCoursePrerequisite as createCoursePrerequisiteApi,
  updateCoursePrerequisite as updateCoursePrerequisiteApi,
  deleteCoursePrerequisite as deleteCoursePrerequisiteApi,
} from '../../services/coursePrerequisiteService';


export const fetchAllCoursePrerequisite = createAsyncThunk(
  'coursePrerequisite/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCoursePrerequisite(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCoursePrerequisite = createAsyncThunk(
  'coursePrerequisite/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCoursePrerequisiteById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCoursePrerequisite = createAsyncThunk(
  'coursePrerequisite/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCoursePrerequisiteApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCoursePrerequisite = createAsyncThunk(
  'coursePrerequisite/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCoursePrerequisiteApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCoursePrerequisite = createAsyncThunk(
  'coursePrerequisite/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCoursePrerequisiteApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const coursePrerequisiteSlice = createSlice({
  name: 'coursePrerequisite',
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
      .addCase(fetchAllCoursePrerequisite.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCoursePrerequisite.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCoursePrerequisite.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCoursePrerequisite.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCoursePrerequisite.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCoursePrerequisite.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCoursePrerequisite.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCoursePrerequisite.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCoursePrerequisite.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCoursePrerequisite.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCoursePrerequisite.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.prerequisiteId === action.payload.prerequisiteId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCoursePrerequisite.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCoursePrerequisite.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCoursePrerequisite.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.prerequisiteId !== action.meta.arg);
      })
      .addCase(removeCoursePrerequisite.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = coursePrerequisiteSlice.actions;
export default coursePrerequisiteSlice.reducer;