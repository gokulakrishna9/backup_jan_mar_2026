import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityEventAttendee,
  getCommunityEventAttendeeById,
  createCommunityEventAttendee as createCommunityEventAttendeeApi,
  updateCommunityEventAttendee as updateCommunityEventAttendeeApi,
  deleteCommunityEventAttendee as deleteCommunityEventAttendeeApi,
} from '../../services/communityEventAttendeeService';


export const fetchAllCommunityEventAttendee = createAsyncThunk(
  'communityEventAttendee/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityEventAttendee(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityEventAttendee = createAsyncThunk(
  'communityEventAttendee/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityEventAttendeeById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityEventAttendee = createAsyncThunk(
  'communityEventAttendee/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityEventAttendeeApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityEventAttendee = createAsyncThunk(
  'communityEventAttendee/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityEventAttendeeApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityEventAttendee = createAsyncThunk(
  'communityEventAttendee/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityEventAttendeeApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityEventAttendeeSlice = createSlice({
  name: 'communityEventAttendee',
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
      .addCase(fetchAllCommunityEventAttendee.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityEventAttendee.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityEventAttendee.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityEventAttendee.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityEventAttendee.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityEventAttendee.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityEventAttendee.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityEventAttendee.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityEventAttendee.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityEventAttendee.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityEventAttendee.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.attendeeId === action.payload.attendeeId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityEventAttendee.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityEventAttendee.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityEventAttendee.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.attendeeId !== action.meta.arg);
      })
      .addCase(removeCommunityEventAttendee.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityEventAttendeeSlice.actions;
export default communityEventAttendeeSlice.reducer;