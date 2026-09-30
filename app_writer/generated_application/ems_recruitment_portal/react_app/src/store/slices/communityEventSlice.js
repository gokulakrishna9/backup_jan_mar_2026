import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityEvent,
  getCommunityEventById,
  createCommunityEvent as createCommunityEventApi,
  updateCommunityEvent as updateCommunityEventApi,
  deleteCommunityEvent as deleteCommunityEventApi,
} from '../../services/communityEventService';


export const fetchAllCommunityEvent = createAsyncThunk(
  'communityEvent/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityEvent(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityEvent = createAsyncThunk(
  'communityEvent/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityEventById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityEvent = createAsyncThunk(
  'communityEvent/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityEventApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityEvent = createAsyncThunk(
  'communityEvent/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityEventApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityEvent = createAsyncThunk(
  'communityEvent/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityEventApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityEventSlice = createSlice({
  name: 'communityEvent',
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
      .addCase(fetchAllCommunityEvent.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityEvent.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityEvent.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityEvent.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityEvent.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityEvent.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityEvent.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityEvent.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityEvent.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityEvent.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityEvent.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.eventId === action.payload.eventId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityEvent.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityEvent.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityEvent.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.eventId !== action.meta.arg);
      })
      .addCase(removeCommunityEvent.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityEventSlice.actions;
export default communityEventSlice.reducer;