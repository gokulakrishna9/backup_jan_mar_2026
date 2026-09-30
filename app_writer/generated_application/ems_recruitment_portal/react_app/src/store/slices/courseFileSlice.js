import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseFile,
  getCourseFileById,
  createCourseFile as createCourseFileApi,
  updateCourseFile as updateCourseFileApi,
  deleteCourseFile as deleteCourseFileApi,
} from '../../services/courseFileService';


export const fetchAllCourseFile = createAsyncThunk(
  'courseFile/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseFile(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseFile = createAsyncThunk(
  'courseFile/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseFileById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseFile = createAsyncThunk(
  'courseFile/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseFileApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseFile = createAsyncThunk(
  'courseFile/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseFileApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseFile = createAsyncThunk(
  'courseFile/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseFileApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseFileSlice = createSlice({
  name: 'courseFile',
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
      .addCase(fetchAllCourseFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseFile.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseFile.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseFile.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.fileId === action.payload.fileId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.fileId !== action.meta.arg);
      })
      .addCase(removeCourseFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseFileSlice.actions;
export default courseFileSlice.reducer;