import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllPostCommentEmogiLink,
  getPostCommentEmogiLinkById,
  createPostCommentEmogiLink as createPostCommentEmogiLinkApi,
  updatePostCommentEmogiLink as updatePostCommentEmogiLinkApi,
  deletePostCommentEmogiLink as deletePostCommentEmogiLinkApi,
} from '../../services/postCommentEmogiLinkService';


export const fetchAllPostCommentEmogiLink = createAsyncThunk(
  'postCommentEmogiLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllPostCommentEmogiLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdPostCommentEmogiLink = createAsyncThunk(
  'postCommentEmogiLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getPostCommentEmogiLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createPostCommentEmogiLink = createAsyncThunk(
  'postCommentEmogiLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createPostCommentEmogiLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updatePostCommentEmogiLink = createAsyncThunk(
  'postCommentEmogiLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updatePostCommentEmogiLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removePostCommentEmogiLink = createAsyncThunk(
  'postCommentEmogiLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deletePostCommentEmogiLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const postCommentEmogiLinkSlice = createSlice({
  name: 'postCommentEmogiLink',
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
      .addCase(fetchAllPostCommentEmogiLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllPostCommentEmogiLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllPostCommentEmogiLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdPostCommentEmogiLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdPostCommentEmogiLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdPostCommentEmogiLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createPostCommentEmogiLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createPostCommentEmogiLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createPostCommentEmogiLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updatePostCommentEmogiLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updatePostCommentEmogiLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updatePostCommentEmogiLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removePostCommentEmogiLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removePostCommentEmogiLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removePostCommentEmogiLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = postCommentEmogiLinkSlice.actions;
export default postCommentEmogiLinkSlice.reducer;