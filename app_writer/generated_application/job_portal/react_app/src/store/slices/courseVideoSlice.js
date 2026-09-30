import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseVideo,
  getCourseVideoById,
  createCourseVideo as createCourseVideoApi,
  updateCourseVideo as updateCourseVideoApi,
  deleteCourseVideo as deleteCourseVideoApi,
} from '../../services/courseVideoService';


export const fetchAllCourseVideo = createAsyncThunk(
  'courseVideo/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseVideo(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseVideo = createAsyncThunk(
  'courseVideo/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseVideoById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseVideo = createAsyncThunk(
  'courseVideo/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseVideoApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseVideo = createAsyncThunk(
  'courseVideo/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseVideoApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseVideo = createAsyncThunk(
  'courseVideo/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseVideoApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseVideoSlice = createSlice({
  name: 'courseVideo',
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
      .addCase(fetchAllCourseVideo.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseVideo.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseVideo.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseVideo.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseVideo.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseVideo.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseVideo.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseVideo.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseVideo.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseVideo.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseVideo.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.courseVideoId === action.payload.courseVideoId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseVideo.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseVideo.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseVideo.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.courseVideoId !== action.meta.arg);
      })
      .addCase(removeCourseVideo.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseVideoSlice.actions;
export default courseVideoSlice.reducer;