import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserPropertyGroup,
  getUserPropertyGroupById,
  createUserPropertyGroup as createUserPropertyGroupApi,
  updateUserPropertyGroup as updateUserPropertyGroupApi,
  deleteUserPropertyGroup as deleteUserPropertyGroupApi,
} from '../../services/userPropertyGroupService';


export const fetchAllUserPropertyGroup = createAsyncThunk(
  'userPropertyGroup/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserPropertyGroup(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserPropertyGroup = createAsyncThunk(
  'userPropertyGroup/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserPropertyGroupById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserPropertyGroup = createAsyncThunk(
  'userPropertyGroup/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserPropertyGroupApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserPropertyGroup = createAsyncThunk(
  'userPropertyGroup/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserPropertyGroupApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserPropertyGroup = createAsyncThunk(
  'userPropertyGroup/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserPropertyGroupApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userPropertyGroupSlice = createSlice({
  name: 'userPropertyGroup',
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
      .addCase(fetchAllUserPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserPropertyGroup.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserPropertyGroup.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.groupId === action.payload.groupId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.groupId !== action.meta.arg);
      })
      .addCase(removeUserPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userPropertyGroupSlice.actions;
export default userPropertyGroupSlice.reducer;