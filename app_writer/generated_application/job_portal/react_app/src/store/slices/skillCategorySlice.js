import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllSkillCategory,
  getSkillCategoryById,
  createSkillCategory as createSkillCategoryApi,
  updateSkillCategory as updateSkillCategoryApi,
  deleteSkillCategory as deleteSkillCategoryApi,
} from '../../services/skillCategoryService';


export const fetchAllSkillCategory = createAsyncThunk(
  'skillCategory/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllSkillCategory(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdSkillCategory = createAsyncThunk(
  'skillCategory/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getSkillCategoryById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createSkillCategory = createAsyncThunk(
  'skillCategory/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createSkillCategoryApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateSkillCategory = createAsyncThunk(
  'skillCategory/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateSkillCategoryApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeSkillCategory = createAsyncThunk(
  'skillCategory/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteSkillCategoryApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const skillCategorySlice = createSlice({
  name: 'skillCategory',
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
      .addCase(fetchAllSkillCategory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllSkillCategory.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllSkillCategory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdSkillCategory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdSkillCategory.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdSkillCategory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createSkillCategory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createSkillCategory.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createSkillCategory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateSkillCategory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateSkillCategory.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.skillCategoryId === action.payload.skillCategoryId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateSkillCategory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeSkillCategory.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeSkillCategory.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.skillCategoryId !== action.meta.arg);
      })
      .addCase(removeSkillCategory.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = skillCategorySlice.actions;
export default skillCategorySlice.reducer;