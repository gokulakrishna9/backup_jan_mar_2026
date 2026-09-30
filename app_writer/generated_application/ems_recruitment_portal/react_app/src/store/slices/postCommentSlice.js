import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllPostComment,
  getPostCommentById,
  createPostComment as createPostCommentApi,
  updatePostComment as updatePostCommentApi,
  deletePostComment as deletePostCommentApi,
} from '../../services/postCommentService';


export const fetchAllPostComment = createAsyncThunk(
  'postComment/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllPostComment(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdPostComment = createAsyncThunk(
  'postComment/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getPostCommentById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createPostComment = createAsyncThunk(
  'postComment/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createPostCommentApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updatePostComment = createAsyncThunk(
  'postComment/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updatePostCommentApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removePostComment = createAsyncThunk(
  'postComment/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deletePostCommentApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const postCommentSlice = createSlice({
  name: 'postComment',
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
      .addCase(fetchAllPostComment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllPostComment.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllPostComment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdPostComment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdPostComment.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdPostComment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createPostComment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createPostComment.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createPostComment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updatePostComment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updatePostComment.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.commentId === action.payload.commentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updatePostComment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removePostComment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removePostComment.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.commentId !== action.meta.arg);
      })
      .addCase(removePostComment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = postCommentSlice.actions;
export default postCommentSlice.reducer;