import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseReview,
  getCourseReviewById,
  createCourseReview as createCourseReviewApi,
  updateCourseReview as updateCourseReviewApi,
  deleteCourseReview as deleteCourseReviewApi,
} from '../../services/courseReviewService';


export const fetchAllCourseReview = createAsyncThunk(
  'courseReview/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseReview(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseReview = createAsyncThunk(
  'courseReview/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseReviewById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseReview = createAsyncThunk(
  'courseReview/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseReviewApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseReview = createAsyncThunk(
  'courseReview/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseReviewApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseReview = createAsyncThunk(
  'courseReview/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseReviewApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseReviewSlice = createSlice({
  name: 'courseReview',
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
      .addCase(fetchAllCourseReview.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseReview.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseReview.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseReview.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseReview.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseReview.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseReview.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseReview.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseReview.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseReview.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseReview.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.reviewId === action.payload.reviewId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseReview.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseReview.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseReview.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.reviewId !== action.meta.arg);
      })
      .addCase(removeCourseReview.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseReviewSlice.actions;
export default courseReviewSlice.reducer;