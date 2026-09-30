import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseCommunityLink,
  getCourseCommunityLinkById,
  createCourseCommunityLink as createCourseCommunityLinkApi,
  updateCourseCommunityLink as updateCourseCommunityLinkApi,
  deleteCourseCommunityLink as deleteCourseCommunityLinkApi,
} from '../../services/courseCommunityLinkService';


export const fetchAllCourseCommunityLink = createAsyncThunk(
  'courseCommunityLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseCommunityLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseCommunityLink = createAsyncThunk(
  'courseCommunityLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseCommunityLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseCommunityLink = createAsyncThunk(
  'courseCommunityLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseCommunityLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseCommunityLink = createAsyncThunk(
  'courseCommunityLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseCommunityLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseCommunityLink = createAsyncThunk(
  'courseCommunityLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseCommunityLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseCommunityLinkSlice = createSlice({
  name: 'courseCommunityLink',
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
      .addCase(fetchAllCourseCommunityLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseCommunityLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseCommunityLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseCommunityLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseCommunityLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseCommunityLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseCommunityLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseCommunityLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseCommunityLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseCommunityLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseCommunityLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseCommunityLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseCommunityLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseCommunityLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeCourseCommunityLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseCommunityLinkSlice.actions;
export default courseCommunityLinkSlice.reducer;