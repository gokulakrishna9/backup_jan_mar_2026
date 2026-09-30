import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllPostFlag,
  getPostFlagById,
  createPostFlag as createPostFlagApi,
  updatePostFlag as updatePostFlagApi,
  deletePostFlag as deletePostFlagApi,
} from '../../services/postFlagService';


export const fetchAllPostFlag = createAsyncThunk(
  'postFlag/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllPostFlag(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdPostFlag = createAsyncThunk(
  'postFlag/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getPostFlagById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createPostFlag = createAsyncThunk(
  'postFlag/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createPostFlagApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updatePostFlag = createAsyncThunk(
  'postFlag/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updatePostFlagApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removePostFlag = createAsyncThunk(
  'postFlag/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deletePostFlagApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const postFlagSlice = createSlice({
  name: 'postFlag',
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
      .addCase(fetchAllPostFlag.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllPostFlag.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllPostFlag.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdPostFlag.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdPostFlag.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdPostFlag.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createPostFlag.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createPostFlag.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createPostFlag.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updatePostFlag.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updatePostFlag.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.flagId === action.payload.flagId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updatePostFlag.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removePostFlag.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removePostFlag.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.flagId !== action.meta.arg);
      })
      .addCase(removePostFlag.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = postFlagSlice.actions;
export default postFlagSlice.reducer;