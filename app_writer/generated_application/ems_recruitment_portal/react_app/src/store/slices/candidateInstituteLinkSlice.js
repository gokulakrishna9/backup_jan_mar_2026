import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCandidateInstituteLink,
  getCandidateInstituteLinkById,
  createCandidateInstituteLink as createCandidateInstituteLinkApi,
  updateCandidateInstituteLink as updateCandidateInstituteLinkApi,
  deleteCandidateInstituteLink as deleteCandidateInstituteLinkApi,
} from '../../services/candidateInstituteLinkService';


export const fetchAllCandidateInstituteLink = createAsyncThunk(
  'candidateInstituteLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCandidateInstituteLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCandidateInstituteLink = createAsyncThunk(
  'candidateInstituteLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCandidateInstituteLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCandidateInstituteLink = createAsyncThunk(
  'candidateInstituteLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCandidateInstituteLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCandidateInstituteLink = createAsyncThunk(
  'candidateInstituteLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCandidateInstituteLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCandidateInstituteLink = createAsyncThunk(
  'candidateInstituteLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCandidateInstituteLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const candidateInstituteLinkSlice = createSlice({
  name: 'candidateInstituteLink',
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
      .addCase(fetchAllCandidateInstituteLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCandidateInstituteLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCandidateInstituteLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCandidateInstituteLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCandidateInstituteLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCandidateInstituteLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCandidateInstituteLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCandidateInstituteLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCandidateInstituteLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCandidateInstituteLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCandidateInstituteLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCandidateInstituteLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCandidateInstituteLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCandidateInstituteLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeCandidateInstituteLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = candidateInstituteLinkSlice.actions;
export default candidateInstituteLinkSlice.reducer;