import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserProfileDocument,
  getUserProfileDocumentById,
  createUserProfileDocument as createUserProfileDocumentApi,
  updateUserProfileDocument as updateUserProfileDocumentApi,
  deleteUserProfileDocument as deleteUserProfileDocumentApi,
} from '../../services/userProfileDocumentService';


export const fetchAllUserProfileDocument = createAsyncThunk(
  'userProfileDocument/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserProfileDocument(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserProfileDocument = createAsyncThunk(
  'userProfileDocument/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserProfileDocumentById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserProfileDocument = createAsyncThunk(
  'userProfileDocument/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserProfileDocumentApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserProfileDocument = createAsyncThunk(
  'userProfileDocument/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserProfileDocumentApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserProfileDocument = createAsyncThunk(
  'userProfileDocument/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserProfileDocumentApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userProfileDocumentSlice = createSlice({
  name: 'userProfileDocument',
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
      .addCase(fetchAllUserProfileDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserProfileDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserProfileDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserProfileDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserProfileDocument.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserProfileDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserProfileDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserProfileDocument.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserProfileDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserProfileDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserProfileDocument.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.documentId === action.payload.documentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserProfileDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserProfileDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserProfileDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.documentId !== action.meta.arg);
      })
      .addCase(removeUserProfileDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userProfileDocumentSlice.actions;
export default userProfileDocumentSlice.reducer;