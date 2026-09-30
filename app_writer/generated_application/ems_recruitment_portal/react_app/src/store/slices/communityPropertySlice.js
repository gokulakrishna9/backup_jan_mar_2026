import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityProperty,
  getCommunityPropertyById,
  createCommunityProperty as createCommunityPropertyApi,
  updateCommunityProperty as updateCommunityPropertyApi,
  deleteCommunityProperty as deleteCommunityPropertyApi,
} from '../../services/communityPropertyService';


export const fetchAllCommunityProperty = createAsyncThunk(
  'communityProperty/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityProperty(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityProperty = createAsyncThunk(
  'communityProperty/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityPropertyById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityProperty = createAsyncThunk(
  'communityProperty/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityPropertyApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityProperty = createAsyncThunk(
  'communityProperty/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityPropertyApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityProperty = createAsyncThunk(
  'communityProperty/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityPropertyApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityPropertySlice = createSlice({
  name: 'communityProperty',
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
      .addCase(fetchAllCommunityProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityProperty.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityProperty.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityProperty.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.propertyId === action.payload.propertyId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.propertyId !== action.meta.arg);
      })
      .addCase(removeCommunityProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityPropertySlice.actions;
export default communityPropertySlice.reducer;