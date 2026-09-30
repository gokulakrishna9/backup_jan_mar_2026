import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserLanguage,
  getUserLanguageById,
  createUserLanguage as createUserLanguageApi,
  updateUserLanguage as updateUserLanguageApi,
  deleteUserLanguage as deleteUserLanguageApi,
} from '../../services/userLanguageService';


export const fetchAllUserLanguage = createAsyncThunk(
  'userLanguage/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserLanguage(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserLanguage = createAsyncThunk(
  'userLanguage/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserLanguageById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserLanguage = createAsyncThunk(
  'userLanguage/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserLanguageApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserLanguage = createAsyncThunk(
  'userLanguage/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserLanguageApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserLanguage = createAsyncThunk(
  'userLanguage/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserLanguageApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userLanguageSlice = createSlice({
  name: 'userLanguage',
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
      .addCase(fetchAllUserLanguage.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserLanguage.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserLanguage.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserLanguage.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserLanguage.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserLanguage.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserLanguage.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserLanguage.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserLanguage.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserLanguage.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserLanguage.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.languageId === action.payload.languageId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserLanguage.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserLanguage.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserLanguage.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.languageId !== action.meta.arg);
      })
      .addCase(removeUserLanguage.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userLanguageSlice.actions;
export default userLanguageSlice.reducer;