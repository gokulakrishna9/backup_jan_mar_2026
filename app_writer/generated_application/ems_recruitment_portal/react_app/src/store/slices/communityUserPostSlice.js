import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityUserPost,
  getCommunityUserPostById,
  createCommunityUserPost as createCommunityUserPostApi,
  updateCommunityUserPost as updateCommunityUserPostApi,
  deleteCommunityUserPost as deleteCommunityUserPostApi,
} from '../../services/communityUserPostService';


export const fetchAllCommunityUserPost = createAsyncThunk(
  'communityUserPost/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityUserPost(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityUserPost = createAsyncThunk(
  'communityUserPost/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityUserPostById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityUserPost = createAsyncThunk(
  'communityUserPost/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityUserPostApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityUserPost = createAsyncThunk(
  'communityUserPost/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityUserPostApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityUserPost = createAsyncThunk(
  'communityUserPost/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityUserPostApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityUserPostSlice = createSlice({
  name: 'communityUserPost',
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
      .addCase(fetchAllCommunityUserPost.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityUserPost.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityUserPost.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityUserPost.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityUserPost.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityUserPost.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityUserPost.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityUserPost.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityUserPost.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityUserPost.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityUserPost.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.postId === action.payload.postId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityUserPost.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityUserPost.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityUserPost.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.postId !== action.meta.arg);
      })
      .addCase(removeCommunityUserPost.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityUserPostSlice.actions;
export default communityUserPostSlice.reducer;