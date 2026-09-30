import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllInstitutionRanking,
  getInstitutionRankingById,
  createInstitutionRanking as createInstitutionRankingApi,
  updateInstitutionRanking as updateInstitutionRankingApi,
  deleteInstitutionRanking as deleteInstitutionRankingApi,
} from '../../services/institutionRankingService';


export const fetchAllInstitutionRanking = createAsyncThunk(
  'institutionRanking/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllInstitutionRanking(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdInstitutionRanking = createAsyncThunk(
  'institutionRanking/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getInstitutionRankingById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createInstitutionRanking = createAsyncThunk(
  'institutionRanking/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createInstitutionRankingApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateInstitutionRanking = createAsyncThunk(
  'institutionRanking/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateInstitutionRankingApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeInstitutionRanking = createAsyncThunk(
  'institutionRanking/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteInstitutionRankingApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const institutionRankingSlice = createSlice({
  name: 'institutionRanking',
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
      .addCase(fetchAllInstitutionRanking.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllInstitutionRanking.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllInstitutionRanking.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdInstitutionRanking.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdInstitutionRanking.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdInstitutionRanking.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createInstitutionRanking.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createInstitutionRanking.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createInstitutionRanking.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateInstitutionRanking.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateInstitutionRanking.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.rankingId === action.payload.rankingId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateInstitutionRanking.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeInstitutionRanking.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeInstitutionRanking.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.rankingId !== action.meta.arg);
      })
      .addCase(removeInstitutionRanking.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = institutionRankingSlice.actions;
export default institutionRankingSlice.reducer;