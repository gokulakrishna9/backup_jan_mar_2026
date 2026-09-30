import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserSkill,
  getUserSkillById,
  createUserSkill as createUserSkillApi,
  updateUserSkill as updateUserSkillApi,
  deleteUserSkill as deleteUserSkillApi,
} from '../../services/userSkillService';


export const fetchAllUserSkill = createAsyncThunk(
  'userSkill/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserSkill(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserSkill = createAsyncThunk(
  'userSkill/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserSkillById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserSkill = createAsyncThunk(
  'userSkill/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserSkillApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserSkill = createAsyncThunk(
  'userSkill/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserSkillApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserSkill = createAsyncThunk(
  'userSkill/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserSkillApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userSkillSlice = createSlice({
  name: 'userSkill',
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
      .addCase(fetchAllUserSkill.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserSkill.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserSkill.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserSkill.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserSkill.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserSkill.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserSkill.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserSkill.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserSkill.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserSkill.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserSkill.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.skillId === action.payload.skillId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserSkill.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserSkill.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserSkill.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.skillId !== action.meta.arg);
      })
      .addCase(removeUserSkill.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userSkillSlice.actions;
export default userSkillSlice.reducer;