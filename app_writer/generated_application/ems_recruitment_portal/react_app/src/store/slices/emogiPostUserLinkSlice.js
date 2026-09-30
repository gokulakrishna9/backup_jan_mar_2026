import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllEmogiPostUserLink,
  getEmogiPostUserLinkById,
  createEmogiPostUserLink as createEmogiPostUserLinkApi,
  updateEmogiPostUserLink as updateEmogiPostUserLinkApi,
  deleteEmogiPostUserLink as deleteEmogiPostUserLinkApi,
} from '../../services/emogiPostUserLinkService';


export const fetchAllEmogiPostUserLink = createAsyncThunk(
  'emogiPostUserLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllEmogiPostUserLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdEmogiPostUserLink = createAsyncThunk(
  'emogiPostUserLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getEmogiPostUserLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createEmogiPostUserLink = createAsyncThunk(
  'emogiPostUserLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createEmogiPostUserLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateEmogiPostUserLink = createAsyncThunk(
  'emogiPostUserLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateEmogiPostUserLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeEmogiPostUserLink = createAsyncThunk(
  'emogiPostUserLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteEmogiPostUserLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const emogiPostUserLinkSlice = createSlice({
  name: 'emogiPostUserLink',
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
      .addCase(fetchAllEmogiPostUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllEmogiPostUserLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllEmogiPostUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdEmogiPostUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdEmogiPostUserLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdEmogiPostUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createEmogiPostUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createEmogiPostUserLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createEmogiPostUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateEmogiPostUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateEmogiPostUserLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateEmogiPostUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeEmogiPostUserLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeEmogiPostUserLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeEmogiPostUserLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = emogiPostUserLinkSlice.actions;
export default emogiPostUserLinkSlice.reducer;