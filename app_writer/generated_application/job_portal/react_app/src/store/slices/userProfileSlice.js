import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserProfile,
  getUserProfileById,
  createUserProfile as createUserProfileApi,
  updateUserProfile as updateUserProfileApi,
  deleteUserProfile as deleteUserProfileApi,
} from '../../services/userProfileService';


export const fetchAllUserProfile = createAsyncThunk(
  'userProfile/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserProfile(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserProfile = createAsyncThunk(
  'userProfile/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserProfileById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserProfile = createAsyncThunk(
  'userProfile/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserProfileApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserProfile = createAsyncThunk(
  'userProfile/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserProfileApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserProfile = createAsyncThunk(
  'userProfile/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserProfileApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userProfileSlice = createSlice({
  name: 'userProfile',
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
      .addCase(fetchAllUserProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserProfile.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserProfile.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserProfile.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.userProfileId === action.payload.userProfileId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.userProfileId !== action.meta.arg);
      })
      .addCase(removeUserProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userProfileSlice.actions;
export default userProfileSlice.reducer;