import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllPostTagLink,
  getPostTagLinkById,
  createPostTagLink as createPostTagLinkApi,
  updatePostTagLink as updatePostTagLinkApi,
  deletePostTagLink as deletePostTagLinkApi,
} from '../../services/postTagLinkService';


export const fetchAllPostTagLink = createAsyncThunk(
  'postTagLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllPostTagLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdPostTagLink = createAsyncThunk(
  'postTagLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getPostTagLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createPostTagLink = createAsyncThunk(
  'postTagLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createPostTagLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updatePostTagLink = createAsyncThunk(
  'postTagLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updatePostTagLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removePostTagLink = createAsyncThunk(
  'postTagLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deletePostTagLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const postTagLinkSlice = createSlice({
  name: 'postTagLink',
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
      .addCase(fetchAllPostTagLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllPostTagLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllPostTagLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdPostTagLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdPostTagLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdPostTagLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createPostTagLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createPostTagLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createPostTagLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updatePostTagLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updatePostTagLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updatePostTagLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removePostTagLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removePostTagLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removePostTagLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = postTagLinkSlice.actions;
export default postTagLinkSlice.reducer;