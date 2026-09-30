import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserFile,
  getUserFileById,
  createUserFile as createUserFileApi,
  updateUserFile as updateUserFileApi,
  deleteUserFile as deleteUserFileApi,
} from '../../services/userFileService';


export const fetchAllUserFile = createAsyncThunk(
  'userFile/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserFile(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserFile = createAsyncThunk(
  'userFile/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserFileById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserFile = createAsyncThunk(
  'userFile/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserFileApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserFile = createAsyncThunk(
  'userFile/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserFileApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserFile = createAsyncThunk(
  'userFile/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserFileApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userFileSlice = createSlice({
  name: 'userFile',
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
      .addCase(fetchAllUserFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserFile.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserFile.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserFile.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.fileId === action.payload.fileId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.fileId !== action.meta.arg);
      })
      .addCase(removeUserFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userFileSlice.actions;
export default userFileSlice.reducer;