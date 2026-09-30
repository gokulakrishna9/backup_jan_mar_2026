import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityPropertyGroup,
  getCommunityPropertyGroupById,
  createCommunityPropertyGroup as createCommunityPropertyGroupApi,
  updateCommunityPropertyGroup as updateCommunityPropertyGroupApi,
  deleteCommunityPropertyGroup as deleteCommunityPropertyGroupApi,
} from '../../services/communityPropertyGroupService';


export const fetchAllCommunityPropertyGroup = createAsyncThunk(
  'communityPropertyGroup/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityPropertyGroup(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityPropertyGroup = createAsyncThunk(
  'communityPropertyGroup/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityPropertyGroupById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityPropertyGroup = createAsyncThunk(
  'communityPropertyGroup/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityPropertyGroupApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityPropertyGroup = createAsyncThunk(
  'communityPropertyGroup/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityPropertyGroupApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityPropertyGroup = createAsyncThunk(
  'communityPropertyGroup/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityPropertyGroupApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityPropertyGroupSlice = createSlice({
  name: 'communityPropertyGroup',
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
      .addCase(fetchAllCommunityPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityPropertyGroup.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityPropertyGroup.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.groupId === action.payload.groupId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.groupId !== action.meta.arg);
      })
      .addCase(removeCommunityPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityPropertyGroupSlice.actions;
export default communityPropertyGroupSlice.reducer;