import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllPostTag,
  getPostTagById,
  createPostTag as createPostTagApi,
  updatePostTag as updatePostTagApi,
  deletePostTag as deletePostTagApi,
} from '../../services/postTagService';


export const fetchAllPostTag = createAsyncThunk(
  'postTag/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllPostTag(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdPostTag = createAsyncThunk(
  'postTag/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getPostTagById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createPostTag = createAsyncThunk(
  'postTag/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createPostTagApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updatePostTag = createAsyncThunk(
  'postTag/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updatePostTagApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removePostTag = createAsyncThunk(
  'postTag/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deletePostTagApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const postTagSlice = createSlice({
  name: 'postTag',
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
      .addCase(fetchAllPostTag.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllPostTag.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllPostTag.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdPostTag.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdPostTag.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdPostTag.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createPostTag.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createPostTag.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createPostTag.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updatePostTag.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updatePostTag.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.tagId === action.payload.tagId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updatePostTag.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removePostTag.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removePostTag.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.tagId !== action.meta.arg);
      })
      .addCase(removePostTag.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = postTagSlice.actions;
export default postTagSlice.reducer;