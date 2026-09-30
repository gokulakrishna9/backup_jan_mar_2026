import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityFile,
  getCommunityFileById,
  createCommunityFile as createCommunityFileApi,
  updateCommunityFile as updateCommunityFileApi,
  deleteCommunityFile as deleteCommunityFileApi,
} from '../../services/communityFileService';


export const fetchAllCommunityFile = createAsyncThunk(
  'communityFile/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityFile(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityFile = createAsyncThunk(
  'communityFile/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityFileById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityFile = createAsyncThunk(
  'communityFile/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityFileApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityFile = createAsyncThunk(
  'communityFile/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityFileApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityFile = createAsyncThunk(
  'communityFile/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityFileApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityFileSlice = createSlice({
  name: 'communityFile',
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
      .addCase(fetchAllCommunityFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityFile.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityFile.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityFile.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.fileId === action.payload.fileId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.fileId !== action.meta.arg);
      })
      .addCase(removeCommunityFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityFileSlice.actions;
export default communityFileSlice.reducer;