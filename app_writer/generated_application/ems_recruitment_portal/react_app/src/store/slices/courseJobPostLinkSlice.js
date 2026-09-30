import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseJobPostLink,
  getCourseJobPostLinkById,
  createCourseJobPostLink as createCourseJobPostLinkApi,
  updateCourseJobPostLink as updateCourseJobPostLinkApi,
  deleteCourseJobPostLink as deleteCourseJobPostLinkApi,
} from '../../services/courseJobPostLinkService';


export const fetchAllCourseJobPostLink = createAsyncThunk(
  'courseJobPostLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseJobPostLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseJobPostLink = createAsyncThunk(
  'courseJobPostLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseJobPostLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseJobPostLink = createAsyncThunk(
  'courseJobPostLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseJobPostLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseJobPostLink = createAsyncThunk(
  'courseJobPostLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseJobPostLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseJobPostLink = createAsyncThunk(
  'courseJobPostLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseJobPostLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseJobPostLinkSlice = createSlice({
  name: 'courseJobPostLink',
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
      .addCase(fetchAllCourseJobPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseJobPostLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseJobPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseJobPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseJobPostLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseJobPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseJobPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseJobPostLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseJobPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseJobPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseJobPostLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseJobPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseJobPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseJobPostLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeCourseJobPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseJobPostLinkSlice.actions;
export default courseJobPostLinkSlice.reducer;