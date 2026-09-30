import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityPropertyUserLink,
  getCommunityPropertyUserLinkById,
  createCommunityPropertyUserLink as createCommunityPropertyUserLinkApi,
  updateCommunityPropertyUserLink as updateCommunityPropertyUserLinkApi,
  deleteCommunityPropertyUserLink as deleteCommunityPropertyUserLinkApi,
} from '../../services/communityPropertyUserLinkService';


export const fetchAllCommunityPropertyUserLink = createAsyncThunk(
  'communityPropertyUserLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityPropertyUserLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityPropertyUserLink = createAsyncThunk(
  'communityPropertyUserLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityPropertyUserLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityPropertyUserLink = createAsyncThunk(
  'communityPropertyUserLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityPropertyUserLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityPropertyUserLink = createAsyncThunk(
  'communityPropertyUserLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityPropertyUserLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityPropertyUserLink = createAsyncThunk(
  'communityPropertyUserLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityPropertyUserLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityPropertyUserLinkSlice = createSlice({
  name: 'communityPropertyUserLink',
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
      .addCase(fetchAllCommunityPropertyUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityPropertyUserLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityPropertyUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityPropertyUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityPropertyUserLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityPropertyUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityPropertyUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityPropertyUserLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityPropertyUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityPropertyUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityPropertyUserLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityPropertyUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityPropertyUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityPropertyUserLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeCommunityPropertyUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityPropertyUserLinkSlice.actions;
export default communityPropertyUserLinkSlice.reducer;