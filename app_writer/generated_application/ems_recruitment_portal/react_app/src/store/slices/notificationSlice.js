import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllNotification,
  getNotificationById,
  createNotification as createNotificationApi,
  updateNotification as updateNotificationApi,
  deleteNotification as deleteNotificationApi,
} from '../../services/notificationService';


export const fetchAllNotification = createAsyncThunk(
  'notification/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllNotification(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdNotification = createAsyncThunk(
  'notification/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getNotificationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createNotification = createAsyncThunk(
  'notification/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createNotificationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateNotification = createAsyncThunk(
  'notification/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateNotificationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeNotification = createAsyncThunk(
  'notification/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteNotificationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const notificationSlice = createSlice({
  name: 'notification',
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
      .addCase(fetchAllNotification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllNotification.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllNotification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdNotification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdNotification.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdNotification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createNotification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createNotification.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createNotification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateNotification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateNotification.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.notificationId === action.payload.notificationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateNotification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeNotification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeNotification.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.notificationId !== action.meta.arg);
      })
      .addCase(removeNotification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = notificationSlice.actions;
export default notificationSlice.reducer;