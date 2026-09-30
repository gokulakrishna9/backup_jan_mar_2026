import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllInstitutionProfileDocument,
  getInstitutionProfileDocumentById,
  createInstitutionProfileDocument as createInstitutionProfileDocumentApi,
  updateInstitutionProfileDocument as updateInstitutionProfileDocumentApi,
  deleteInstitutionProfileDocument as deleteInstitutionProfileDocumentApi,
} from '../../services/institutionProfileDocumentService';


export const fetchAllInstitutionProfileDocument = createAsyncThunk(
  'institutionProfileDocument/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllInstitutionProfileDocument(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdInstitutionProfileDocument = createAsyncThunk(
  'institutionProfileDocument/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getInstitutionProfileDocumentById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createInstitutionProfileDocument = createAsyncThunk(
  'institutionProfileDocument/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createInstitutionProfileDocumentApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateInstitutionProfileDocument = createAsyncThunk(
  'institutionProfileDocument/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateInstitutionProfileDocumentApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeInstitutionProfileDocument = createAsyncThunk(
  'institutionProfileDocument/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteInstitutionProfileDocumentApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const institutionProfileDocumentSlice = createSlice({
  name: 'institutionProfileDocument',
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
      .addCase(fetchAllInstitutionProfileDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllInstitutionProfileDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllInstitutionProfileDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdInstitutionProfileDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdInstitutionProfileDocument.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdInstitutionProfileDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createInstitutionProfileDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createInstitutionProfileDocument.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createInstitutionProfileDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateInstitutionProfileDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateInstitutionProfileDocument.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.documentId === action.payload.documentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateInstitutionProfileDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeInstitutionProfileDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeInstitutionProfileDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.documentId !== action.meta.arg);
      })
      .addCase(removeInstitutionProfileDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = institutionProfileDocumentSlice.actions;
export default institutionProfileDocumentSlice.reducer;