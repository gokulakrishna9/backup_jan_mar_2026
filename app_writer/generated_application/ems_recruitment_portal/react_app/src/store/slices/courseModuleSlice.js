import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseModule,
  getCourseModuleById,
  createCourseModule as createCourseModuleApi,
  updateCourseModule as updateCourseModuleApi,
  deleteCourseModule as deleteCourseModuleApi,
} from '../../services/courseModuleService';


export const fetchAllCourseModule = createAsyncThunk(
  'courseModule/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseModule(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseModule = createAsyncThunk(
  'courseModule/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseModuleById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseModule = createAsyncThunk(
  'courseModule/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseModuleApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseModule = createAsyncThunk(
  'courseModule/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseModuleApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseModule = createAsyncThunk(
  'courseModule/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseModuleApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseModuleSlice = createSlice({
  name: 'courseModule',
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
      .addCase(fetchAllCourseModule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseModule.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseModule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseModule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseModule.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseModule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseModule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseModule.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseModule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseModule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseModule.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.moduleId === action.payload.moduleId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseModule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseModule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseModule.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.moduleId !== action.meta.arg);
      })
      .addCase(removeCourseModule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseModuleSlice.actions;
export default courseModuleSlice.reducer;