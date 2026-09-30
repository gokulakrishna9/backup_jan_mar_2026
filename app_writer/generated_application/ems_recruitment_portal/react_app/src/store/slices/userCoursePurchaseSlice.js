import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserCoursePurchase,
  getUserCoursePurchaseById,
  createUserCoursePurchase as createUserCoursePurchaseApi,
  updateUserCoursePurchase as updateUserCoursePurchaseApi,
  deleteUserCoursePurchase as deleteUserCoursePurchaseApi,
} from '../../services/userCoursePurchaseService';


export const fetchAllUserCoursePurchase = createAsyncThunk(
  'userCoursePurchase/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserCoursePurchase(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserCoursePurchase = createAsyncThunk(
  'userCoursePurchase/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserCoursePurchaseById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserCoursePurchase = createAsyncThunk(
  'userCoursePurchase/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserCoursePurchaseApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserCoursePurchase = createAsyncThunk(
  'userCoursePurchase/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserCoursePurchaseApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserCoursePurchase = createAsyncThunk(
  'userCoursePurchase/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserCoursePurchaseApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userCoursePurchaseSlice = createSlice({
  name: 'userCoursePurchase',
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
      .addCase(fetchAllUserCoursePurchase.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserCoursePurchase.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserCoursePurchase.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserCoursePurchase.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserCoursePurchase.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserCoursePurchase.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserCoursePurchase.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserCoursePurchase.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserCoursePurchase.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserCoursePurchase.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserCoursePurchase.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.purchaseId === action.payload.purchaseId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserCoursePurchase.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserCoursePurchase.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserCoursePurchase.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.purchaseId !== action.meta.arg);
      })
      .addCase(removeUserCoursePurchase.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userCoursePurchaseSlice.actions;
export default userCoursePurchaseSlice.reducer;