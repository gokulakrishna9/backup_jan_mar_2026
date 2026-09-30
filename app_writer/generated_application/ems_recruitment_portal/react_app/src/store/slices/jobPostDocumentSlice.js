import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPostDocument,
  getJobPostDocumentById,
  createJobPostDocument as createJobPostDocumentApi,
  updateJobPostDocument as updateJobPostDocumentApi,
  deleteJobPostDocument as deleteJobPostDocumentApi,
} from '../../services/jobPostDocumentService';


export const fetchAllJobPostDocument = createAsyncThunk(
  'jobPostDocument/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPostDocument(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPostDocument = createAsyncThunk(
  'jobPostDocument/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostDocumentById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPostDocument = createAsyncThunk(
  'jobPostDocument/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostDocumentApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPostDocument = createAsyncThunk(
  'jobPostDocument/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostDocumentApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPostDocument = createAsyncThunk(
  'jobPostDocument/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostDocumentApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostDocumentSlice = createSlice({
  name: 'jobPostDocument',
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
      .addCase(fetchAllJobPostDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPostDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPostDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPostDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPostDocument.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPostDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPostDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPostDocument.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPostDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPostDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPostDocument.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.documentId === action.payload.documentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPostDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPostDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPostDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.documentId !== action.meta.arg);
      })
      .addCase(removeJobPostDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostDocumentSlice.actions;
export default jobPostDocumentSlice.reducer;