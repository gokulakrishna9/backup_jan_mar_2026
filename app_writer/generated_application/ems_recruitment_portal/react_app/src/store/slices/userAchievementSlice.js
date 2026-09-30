import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserAchievement,
  getUserAchievementById,
  createUserAchievement as createUserAchievementApi,
  updateUserAchievement as updateUserAchievementApi,
  deleteUserAchievement as deleteUserAchievementApi,
} from '../../services/userAchievementService';


export const fetchAllUserAchievement = createAsyncThunk(
  'userAchievement/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserAchievement(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserAchievement = createAsyncThunk(
  'userAchievement/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserAchievementById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserAchievement = createAsyncThunk(
  'userAchievement/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserAchievementApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserAchievement = createAsyncThunk(
  'userAchievement/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserAchievementApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserAchievement = createAsyncThunk(
  'userAchievement/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserAchievementApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userAchievementSlice = createSlice({
  name: 'userAchievement',
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
      .addCase(fetchAllUserAchievement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserAchievement.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserAchievement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserAchievement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserAchievement.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserAchievement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserAchievement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserAchievement.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserAchievement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserAchievement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserAchievement.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.achievementId === action.payload.achievementId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserAchievement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserAchievement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserAchievement.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.achievementId !== action.meta.arg);
      })
      .addCase(removeUserAchievement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userAchievementSlice.actions;
export default userAchievementSlice.reducer;