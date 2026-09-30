import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseDocument,
  getCourseDocumentById,
  createCourseDocument as createCourseDocumentApi,
  updateCourseDocument as updateCourseDocumentApi,
  deleteCourseDocument as deleteCourseDocumentApi,
} from '../../services/courseDocumentService';


export const fetchAllCourseDocument = createAsyncThunk(
  'courseDocument/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseDocument(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseDocument = createAsyncThunk(
  'courseDocument/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseDocumentById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseDocument = createAsyncThunk(
  'courseDocument/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseDocumentApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseDocument = createAsyncThunk(
  'courseDocument/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseDocumentApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseDocument = createAsyncThunk(
  'courseDocument/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseDocumentApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseDocumentSlice = createSlice({
  name: 'courseDocument',
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
      .addCase(fetchAllCourseDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseDocument.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseDocument.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseDocument.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.documentId === action.payload.documentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.documentId !== action.meta.arg);
      })
      .addCase(removeCourseDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseDocumentSlice.actions;
export default courseDocumentSlice.reducer;