import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllLocation,
  getLocationById,
  createLocation as createLocationApi,
  updateLocation as updateLocationApi,
  deleteLocation as deleteLocationApi,
} from '../../services/locationService';


export const fetchAllLocation = createAsyncThunk(
  'location/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllLocation(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdLocation = createAsyncThunk(
  'location/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getLocationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createLocation = createAsyncThunk(
  'location/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createLocationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateLocation = createAsyncThunk(
  'location/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateLocationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeLocation = createAsyncThunk(
  'location/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteLocationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const locationSlice = createSlice({
  name: 'location',
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
      .addCase(fetchAllLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllLocation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdLocation.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createLocation.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateLocation.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.locationId === action.payload.locationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeLocation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.locationId !== action.meta.arg);
      })
      .addCase(removeLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = locationSlice.actions;
export default locationSlice.reducer;