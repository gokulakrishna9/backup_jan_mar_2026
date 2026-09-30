import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityCategory,
  getCommunityCategoryById,
  createCommunityCategory as createCommunityCategoryApi,
  updateCommunityCategory as updateCommunityCategoryApi,
  deleteCommunityCategory as deleteCommunityCategoryApi,
} from '../../services/communityCategoryService';


export const fetchAllCommunityCategory = createAsyncThunk(
  'communityCategory/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityCategory(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityCategory = createAsyncThunk(
  'communityCategory/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityCategoryById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityCategory = createAsyncThunk(
  'communityCategory/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityCategoryApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityCategory = createAsyncThunk(
  'communityCategory/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityCategoryApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityCategory = createAsyncThunk(
  'communityCategory/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityCategoryApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityCategorySlice = createSlice({
  name: 'communityCategory',
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
      .addCase(fetchAllCommunityCategory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityCategory.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityCategory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityCategory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityCategory.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityCategory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityCategory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityCategory.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityCategory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityCategory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityCategory.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.categoryId === action.payload.categoryId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityCategory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityCategory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityCategory.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.categoryId !== action.meta.arg);
      })
      .addCase(removeCommunityCategory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityCategorySlice.actions;
export default communityCategorySlice.reducer;