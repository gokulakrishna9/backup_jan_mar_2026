import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserSkillEndorsement,
  getUserSkillEndorsementById,
  createUserSkillEndorsement as createUserSkillEndorsementApi,
  updateUserSkillEndorsement as updateUserSkillEndorsementApi,
  deleteUserSkillEndorsement as deleteUserSkillEndorsementApi,
} from '../../services/userSkillEndorsementService';


export const fetchAllUserSkillEndorsement = createAsyncThunk(
  'userSkillEndorsement/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserSkillEndorsement(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserSkillEndorsement = createAsyncThunk(
  'userSkillEndorsement/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserSkillEndorsementById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserSkillEndorsement = createAsyncThunk(
  'userSkillEndorsement/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserSkillEndorsementApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserSkillEndorsement = createAsyncThunk(
  'userSkillEndorsement/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserSkillEndorsementApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserSkillEndorsement = createAsyncThunk(
  'userSkillEndorsement/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserSkillEndorsementApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userSkillEndorsementSlice = createSlice({
  name: 'userSkillEndorsement',
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
      .addCase(fetchAllUserSkillEndorsement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserSkillEndorsement.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserSkillEndorsement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserSkillEndorsement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserSkillEndorsement.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserSkillEndorsement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserSkillEndorsement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserSkillEndorsement.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserSkillEndorsement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserSkillEndorsement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserSkillEndorsement.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.endorsementId === action.payload.endorsementId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserSkillEndorsement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserSkillEndorsement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserSkillEndorsement.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.endorsementId !== action.meta.arg);
      })
      .addCase(removeUserSkillEndorsement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userSkillEndorsementSlice.actions;
export default userSkillEndorsementSlice.reducer;