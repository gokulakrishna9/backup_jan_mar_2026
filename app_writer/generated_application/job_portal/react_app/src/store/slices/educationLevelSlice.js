import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllEducationLevel,
  getEducationLevelById,
  createEducationLevel as createEducationLevelApi,
  updateEducationLevel as updateEducationLevelApi,
  deleteEducationLevel as deleteEducationLevelApi,
} from '../../services/educationLevelService';


export const fetchAllEducationLevel = createAsyncThunk(
  'educationLevel/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllEducationLevel(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdEducationLevel = createAsyncThunk(
  'educationLevel/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getEducationLevelById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createEducationLevel = createAsyncThunk(
  'educationLevel/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createEducationLevelApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateEducationLevel = createAsyncThunk(
  'educationLevel/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateEducationLevelApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeEducationLevel = createAsyncThunk(
  'educationLevel/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteEducationLevelApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const educationLevelSlice = createSlice({
  name: 'educationLevel',
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
      .addCase(fetchAllEducationLevel.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllEducationLevel.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllEducationLevel.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdEducationLevel.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdEducationLevel.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdEducationLevel.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createEducationLevel.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createEducationLevel.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createEducationLevel.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateEducationLevel.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateEducationLevel.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.educationLevelId === action.payload.educationLevelId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateEducationLevel.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeEducationLevel.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeEducationLevel.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.educationLevelId !== action.meta.arg);
      })
      .addCase(removeEducationLevel.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = educationLevelSlice.actions;
export default educationLevelSlice.reducer;