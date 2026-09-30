import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllTrainerProfile,
  getTrainerProfileById,
  createTrainerProfile as createTrainerProfileApi,
  updateTrainerProfile as updateTrainerProfileApi,
  deleteTrainerProfile as deleteTrainerProfileApi,
} from '../../services/trainerProfileService';


export const fetchAllTrainerProfile = createAsyncThunk(
  'trainerProfile/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllTrainerProfile(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdTrainerProfile = createAsyncThunk(
  'trainerProfile/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getTrainerProfileById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createTrainerProfile = createAsyncThunk(
  'trainerProfile/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createTrainerProfileApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateTrainerProfile = createAsyncThunk(
  'trainerProfile/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateTrainerProfileApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeTrainerProfile = createAsyncThunk(
  'trainerProfile/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteTrainerProfileApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const trainerProfileSlice = createSlice({
  name: 'trainerProfile',
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
      .addCase(fetchAllTrainerProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllTrainerProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllTrainerProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdTrainerProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdTrainerProfile.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdTrainerProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createTrainerProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createTrainerProfile.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createTrainerProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateTrainerProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateTrainerProfile.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.trainerProfileId === action.payload.trainerProfileId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateTrainerProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeTrainerProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeTrainerProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.trainerProfileId !== action.meta.arg);
      })
      .addCase(removeTrainerProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = trainerProfileSlice.actions;
export default trainerProfileSlice.reducer;