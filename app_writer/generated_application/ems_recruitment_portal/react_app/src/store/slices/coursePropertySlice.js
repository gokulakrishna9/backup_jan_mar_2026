import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseProperty,
  getCoursePropertyById,
  createCourseProperty as createCoursePropertyApi,
  updateCourseProperty as updateCoursePropertyApi,
  deleteCourseProperty as deleteCoursePropertyApi,
} from '../../services/coursePropertyService';


export const fetchAllCourseProperty = createAsyncThunk(
  'courseProperty/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseProperty(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseProperty = createAsyncThunk(
  'courseProperty/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCoursePropertyById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseProperty = createAsyncThunk(
  'courseProperty/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCoursePropertyApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseProperty = createAsyncThunk(
  'courseProperty/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCoursePropertyApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseProperty = createAsyncThunk(
  'courseProperty/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCoursePropertyApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const coursePropertySlice = createSlice({
  name: 'courseProperty',
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
      .addCase(fetchAllCourseProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseProperty.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseProperty.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseProperty.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.propertyId === action.payload.propertyId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.propertyId !== action.meta.arg);
      })
      .addCase(removeCourseProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = coursePropertySlice.actions;
export default coursePropertySlice.reducer;