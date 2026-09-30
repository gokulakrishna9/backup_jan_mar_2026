import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllPostEmogi,
  getPostEmogiById,
  createPostEmogi as createPostEmogiApi,
  updatePostEmogi as updatePostEmogiApi,
  deletePostEmogi as deletePostEmogiApi,
} from '../../services/postEmogiService';


export const fetchAllPostEmogi = createAsyncThunk(
  'postEmogi/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllPostEmogi(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdPostEmogi = createAsyncThunk(
  'postEmogi/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getPostEmogiById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createPostEmogi = createAsyncThunk(
  'postEmogi/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createPostEmogiApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updatePostEmogi = createAsyncThunk(
  'postEmogi/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updatePostEmogiApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removePostEmogi = createAsyncThunk(
  'postEmogi/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deletePostEmogiApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const postEmogiSlice = createSlice({
  name: 'postEmogi',
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
      .addCase(fetchAllPostEmogi.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllPostEmogi.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllPostEmogi.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdPostEmogi.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdPostEmogi.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdPostEmogi.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createPostEmogi.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createPostEmogi.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createPostEmogi.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updatePostEmogi.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updatePostEmogi.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.emogiId === action.payload.emogiId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updatePostEmogi.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removePostEmogi.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removePostEmogi.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.emogiId !== action.meta.arg);
      })
      .addCase(removePostEmogi.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = postEmogiSlice.actions;
export default postEmogiSlice.reducer;