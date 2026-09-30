import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserJobPostBookmark,
  getUserJobPostBookmarkById,
  createUserJobPostBookmark as createUserJobPostBookmarkApi,
  updateUserJobPostBookmark as updateUserJobPostBookmarkApi,
  deleteUserJobPostBookmark as deleteUserJobPostBookmarkApi,
} from '../../services/userJobPostBookmarkService';


export const fetchAllUserJobPostBookmark = createAsyncThunk(
  'userJobPostBookmark/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserJobPostBookmark(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserJobPostBookmark = createAsyncThunk(
  'userJobPostBookmark/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserJobPostBookmarkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserJobPostBookmark = createAsyncThunk(
  'userJobPostBookmark/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserJobPostBookmarkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserJobPostBookmark = createAsyncThunk(
  'userJobPostBookmark/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserJobPostBookmarkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserJobPostBookmark = createAsyncThunk(
  'userJobPostBookmark/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserJobPostBookmarkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userJobPostBookmarkSlice = createSlice({
  name: 'userJobPostBookmark',
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
      .addCase(fetchAllUserJobPostBookmark.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserJobPostBookmark.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserJobPostBookmark.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserJobPostBookmark.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserJobPostBookmark.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserJobPostBookmark.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserJobPostBookmark.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserJobPostBookmark.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserJobPostBookmark.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserJobPostBookmark.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserJobPostBookmark.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.bookmarkId === action.payload.bookmarkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserJobPostBookmark.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserJobPostBookmark.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserJobPostBookmark.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.bookmarkId !== action.meta.arg);
      })
      .addCase(removeUserJobPostBookmark.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userJobPostBookmarkSlice.actions;
export default userJobPostBookmarkSlice.reducer;