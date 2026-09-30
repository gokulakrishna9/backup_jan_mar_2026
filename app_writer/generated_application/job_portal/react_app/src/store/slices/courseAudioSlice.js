import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseAudio,
  getCourseAudioById,
  createCourseAudio as createCourseAudioApi,
  updateCourseAudio as updateCourseAudioApi,
  deleteCourseAudio as deleteCourseAudioApi,
} from '../../services/courseAudioService';


export const fetchAllCourseAudio = createAsyncThunk(
  'courseAudio/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseAudio(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseAudio = createAsyncThunk(
  'courseAudio/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseAudioById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseAudio = createAsyncThunk(
  'courseAudio/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseAudioApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseAudio = createAsyncThunk(
  'courseAudio/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseAudioApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseAudio = createAsyncThunk(
  'courseAudio/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseAudioApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseAudioSlice = createSlice({
  name: 'courseAudio',
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
      .addCase(fetchAllCourseAudio.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseAudio.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseAudio.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseAudio.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseAudio.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseAudio.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseAudio.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseAudio.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseAudio.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseAudio.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseAudio.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.courseAudioId === action.payload.courseAudioId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseAudio.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseAudio.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseAudio.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.courseAudioId !== action.meta.arg);
      })
      .addCase(removeCourseAudio.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseAudioSlice.actions;
export default courseAudioSlice.reducer;