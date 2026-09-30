import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserProperty,
  getUserPropertyById,
  createUserProperty as createUserPropertyApi,
  updateUserProperty as updateUserPropertyApi,
  deleteUserProperty as deleteUserPropertyApi,
} from '../../services/userPropertyService';


export const fetchAllUserProperty = createAsyncThunk(
  'userProperty/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserProperty(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserProperty = createAsyncThunk(
  'userProperty/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserPropertyById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserProperty = createAsyncThunk(
  'userProperty/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserPropertyApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserProperty = createAsyncThunk(
  'userProperty/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserPropertyApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserProperty = createAsyncThunk(
  'userProperty/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserPropertyApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userPropertySlice = createSlice({
  name: 'userProperty',
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
      .addCase(fetchAllUserProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserProperty.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserProperty.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserProperty.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.propertyId === action.payload.propertyId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.propertyId !== action.meta.arg);
      })
      .addCase(removeUserProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userPropertySlice.actions;
export default userPropertySlice.reducer;