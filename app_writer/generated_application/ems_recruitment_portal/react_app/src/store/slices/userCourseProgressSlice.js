import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserCourseProgress,
  getUserCourseProgressById,
  createUserCourseProgress as createUserCourseProgressApi,
  updateUserCourseProgress as updateUserCourseProgressApi,
  deleteUserCourseProgress as deleteUserCourseProgressApi,
} from '../../services/userCourseProgressService';


export const fetchAllUserCourseProgress = createAsyncThunk(
  'userCourseProgress/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserCourseProgress(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserCourseProgress = createAsyncThunk(
  'userCourseProgress/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserCourseProgressById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserCourseProgress = createAsyncThunk(
  'userCourseProgress/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserCourseProgressApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserCourseProgress = createAsyncThunk(
  'userCourseProgress/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserCourseProgressApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserCourseProgress = createAsyncThunk(
  'userCourseProgress/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserCourseProgressApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userCourseProgressSlice = createSlice({
  name: 'userCourseProgress',
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
      .addCase(fetchAllUserCourseProgress.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserCourseProgress.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserCourseProgress.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserCourseProgress.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserCourseProgress.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserCourseProgress.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserCourseProgress.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserCourseProgress.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserCourseProgress.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserCourseProgress.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserCourseProgress.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.progressId === action.payload.progressId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserCourseProgress.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserCourseProgress.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserCourseProgress.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.progressId !== action.meta.arg);
      })
      .addCase(removeUserCourseProgress.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userCourseProgressSlice.actions;
export default userCourseProgressSlice.reducer;