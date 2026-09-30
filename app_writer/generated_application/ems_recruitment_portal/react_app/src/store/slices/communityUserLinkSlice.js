import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityUserLink,
  getCommunityUserLinkById,
  createCommunityUserLink as createCommunityUserLinkApi,
  updateCommunityUserLink as updateCommunityUserLinkApi,
  deleteCommunityUserLink as deleteCommunityUserLinkApi,
} from '../../services/communityUserLinkService';


export const fetchAllCommunityUserLink = createAsyncThunk(
  'communityUserLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityUserLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityUserLink = createAsyncThunk(
  'communityUserLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityUserLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityUserLink = createAsyncThunk(
  'communityUserLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityUserLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityUserLink = createAsyncThunk(
  'communityUserLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityUserLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityUserLink = createAsyncThunk(
  'communityUserLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityUserLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityUserLinkSlice = createSlice({
  name: 'communityUserLink',
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
      .addCase(fetchAllCommunityUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityUserLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityUserLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityUserLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityUserLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityUserLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeCommunityUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityUserLinkSlice.actions;
export default communityUserLinkSlice.reducer;