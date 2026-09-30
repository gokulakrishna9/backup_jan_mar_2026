import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUser,
  getUserById,
  createUser as createUserApi,
  updateUser as updateUserApi,
  deleteUser as deleteUserApi,
} from '../../services/userService';


export const fetchAllUser = createAsyncThunk(
  'user/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUser(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUser = createAsyncThunk(
  'user/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUser = createAsyncThunk(
  'user/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUser = createAsyncThunk(
  'user/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUser = createAsyncThunk(
  'user/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userSlice = createSlice({
  name: 'user',
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
      .addCase(fetchAllUser.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUser.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUser.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUser.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUser.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUser.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUser.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUser.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUser.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUser.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUser.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.userId === action.payload.userId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUser.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUser.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUser.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.userId !== action.meta.arg);
      })
      .addCase(removeUser.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userSlice.actions;
export default userSlice.reducer;