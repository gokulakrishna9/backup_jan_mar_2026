import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserWorkExperience,
  getUserWorkExperienceById,
  createUserWorkExperience as createUserWorkExperienceApi,
  updateUserWorkExperience as updateUserWorkExperienceApi,
  deleteUserWorkExperience as deleteUserWorkExperienceApi,
} from '../../services/userWorkExperienceService';


export const fetchAllUserWorkExperience = createAsyncThunk(
  'userWorkExperience/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserWorkExperience(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserWorkExperience = createAsyncThunk(
  'userWorkExperience/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserWorkExperienceById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserWorkExperience = createAsyncThunk(
  'userWorkExperience/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserWorkExperienceApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserWorkExperience = createAsyncThunk(
  'userWorkExperience/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserWorkExperienceApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserWorkExperience = createAsyncThunk(
  'userWorkExperience/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserWorkExperienceApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userWorkExperienceSlice = createSlice({
  name: 'userWorkExperience',
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
      .addCase(fetchAllUserWorkExperience.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserWorkExperience.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserWorkExperience.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserWorkExperience.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserWorkExperience.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserWorkExperience.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserWorkExperience.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserWorkExperience.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserWorkExperience.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserWorkExperience.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserWorkExperience.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.experienceId === action.payload.experienceId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserWorkExperience.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserWorkExperience.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserWorkExperience.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.experienceId !== action.meta.arg);
      })
      .addCase(removeUserWorkExperience.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userWorkExperienceSlice.actions;
export default userWorkExperienceSlice.reducer;