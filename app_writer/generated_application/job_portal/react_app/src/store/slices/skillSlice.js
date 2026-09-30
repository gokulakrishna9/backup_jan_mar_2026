import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllSkill,
  getSkillById,
  createSkill as createSkillApi,
  updateSkill as updateSkillApi,
  deleteSkill as deleteSkillApi,
} from '../../services/skillService';


export const fetchAllSkill = createAsyncThunk(
  'skill/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllSkill(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdSkill = createAsyncThunk(
  'skill/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getSkillById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createSkill = createAsyncThunk(
  'skill/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createSkillApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateSkill = createAsyncThunk(
  'skill/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateSkillApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeSkill = createAsyncThunk(
  'skill/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteSkillApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const skillSlice = createSlice({
  name: 'skill',
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
      .addCase(fetchAllSkill.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllSkill.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllSkill.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdSkill.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdSkill.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdSkill.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createSkill.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createSkill.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createSkill.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateSkill.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateSkill.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.skillId === action.payload.skillId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateSkill.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeSkill.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeSkill.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.skillId !== action.meta.arg);
      })
      .addCase(removeSkill.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = skillSlice.actions;
export default skillSlice.reducer;