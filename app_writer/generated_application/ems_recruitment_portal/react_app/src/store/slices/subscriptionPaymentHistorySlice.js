import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllSubscriptionPaymentHistory,
  getSubscriptionPaymentHistoryById,
  createSubscriptionPaymentHistory as createSubscriptionPaymentHistoryApi,
  updateSubscriptionPaymentHistory as updateSubscriptionPaymentHistoryApi,
  deleteSubscriptionPaymentHistory as deleteSubscriptionPaymentHistoryApi,
} from '../../services/subscriptionPaymentHistoryService';


export const fetchAllSubscriptionPaymentHistory = createAsyncThunk(
  'subscriptionPaymentHistory/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllSubscriptionPaymentHistory(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdSubscriptionPaymentHistory = createAsyncThunk(
  'subscriptionPaymentHistory/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getSubscriptionPaymentHistoryById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createSubscriptionPaymentHistory = createAsyncThunk(
  'subscriptionPaymentHistory/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createSubscriptionPaymentHistoryApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateSubscriptionPaymentHistory = createAsyncThunk(
  'subscriptionPaymentHistory/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateSubscriptionPaymentHistoryApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeSubscriptionPaymentHistory = createAsyncThunk(
  'subscriptionPaymentHistory/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteSubscriptionPaymentHistoryApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const subscriptionPaymentHistorySlice = createSlice({
  name: 'subscriptionPaymentHistory',
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
      .addCase(fetchAllSubscriptionPaymentHistory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllSubscriptionPaymentHistory.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllSubscriptionPaymentHistory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdSubscriptionPaymentHistory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdSubscriptionPaymentHistory.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdSubscriptionPaymentHistory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createSubscriptionPaymentHistory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createSubscriptionPaymentHistory.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createSubscriptionPaymentHistory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateSubscriptionPaymentHistory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateSubscriptionPaymentHistory.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.paymentId === action.payload.paymentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateSubscriptionPaymentHistory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeSubscriptionPaymentHistory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeSubscriptionPaymentHistory.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.paymentId !== action.meta.arg);
      })
      .addCase(removeSubscriptionPaymentHistory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = subscriptionPaymentHistorySlice.actions;
export default subscriptionPaymentHistorySlice.reducer;