import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserRecommendation,
  getUserRecommendationById,
  createUserRecommendation as createUserRecommendationApi,
  updateUserRecommendation as updateUserRecommendationApi,
  deleteUserRecommendation as deleteUserRecommendationApi,
} from '../../services/userRecommendationService';


export const fetchAllUserRecommendation = createAsyncThunk(
  'userRecommendation/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserRecommendation(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserRecommendation = createAsyncThunk(
  'userRecommendation/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserRecommendationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserRecommendation = createAsyncThunk(
  'userRecommendation/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserRecommendationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserRecommendation = createAsyncThunk(
  'userRecommendation/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserRecommendationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserRecommendation = createAsyncThunk(
  'userRecommendation/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserRecommendationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userRecommendationSlice = createSlice({
  name: 'userRecommendation',
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
      .addCase(fetchAllUserRecommendation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserRecommendation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserRecommendation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserRecommendation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserRecommendation.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserRecommendation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserRecommendation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserRecommendation.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserRecommendation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserRecommendation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserRecommendation.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.recommendationId === action.payload.recommendationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserRecommendation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserRecommendation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserRecommendation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.recommendationId !== action.meta.arg);
      })
      .addCase(removeUserRecommendation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userRecommendationSlice.actions;
export default userRecommendationSlice.reducer;