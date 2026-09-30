import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserEducation,
  getUserEducationById,
  createUserEducation as createUserEducationApi,
  updateUserEducation as updateUserEducationApi,
  deleteUserEducation as deleteUserEducationApi,
} from '../../services/userEducationService';


export const fetchAllUserEducation = createAsyncThunk(
  'userEducation/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserEducation(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserEducation = createAsyncThunk(
  'userEducation/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserEducationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserEducation = createAsyncThunk(
  'userEducation/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserEducationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserEducation = createAsyncThunk(
  'userEducation/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserEducationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserEducation = createAsyncThunk(
  'userEducation/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserEducationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userEducationSlice = createSlice({
  name: 'userEducation',
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
      .addCase(fetchAllUserEducation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserEducation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserEducation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserEducation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserEducation.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserEducation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserEducation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserEducation.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserEducation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserEducation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserEducation.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.educationId === action.payload.educationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserEducation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserEducation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserEducation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.educationId !== action.meta.arg);
      })
      .addCase(removeUserEducation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userEducationSlice.actions;
export default userEducationSlice.reducer;