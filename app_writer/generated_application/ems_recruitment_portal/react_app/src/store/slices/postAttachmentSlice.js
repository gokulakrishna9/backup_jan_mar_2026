import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllPostAttachment,
  getPostAttachmentById,
  createPostAttachment as createPostAttachmentApi,
  updatePostAttachment as updatePostAttachmentApi,
  deletePostAttachment as deletePostAttachmentApi,
} from '../../services/postAttachmentService';


export const fetchAllPostAttachment = createAsyncThunk(
  'postAttachment/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllPostAttachment(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdPostAttachment = createAsyncThunk(
  'postAttachment/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getPostAttachmentById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createPostAttachment = createAsyncThunk(
  'postAttachment/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createPostAttachmentApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updatePostAttachment = createAsyncThunk(
  'postAttachment/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updatePostAttachmentApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removePostAttachment = createAsyncThunk(
  'postAttachment/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deletePostAttachmentApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const postAttachmentSlice = createSlice({
  name: 'postAttachment',
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
      .addCase(fetchAllPostAttachment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllPostAttachment.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllPostAttachment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdPostAttachment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdPostAttachment.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdPostAttachment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createPostAttachment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createPostAttachment.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createPostAttachment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updatePostAttachment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updatePostAttachment.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.attachmentId === action.payload.attachmentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updatePostAttachment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removePostAttachment.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removePostAttachment.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.attachmentId !== action.meta.arg);
      })
      .addCase(removePostAttachment.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = postAttachmentSlice.actions;
export default postAttachmentSlice.reducer;