import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllMarketTrendCourseLink,
  getMarketTrendCourseLinkById,
  createMarketTrendCourseLink as createMarketTrendCourseLinkApi,
  updateMarketTrendCourseLink as updateMarketTrendCourseLinkApi,
  deleteMarketTrendCourseLink as deleteMarketTrendCourseLinkApi,
} from '../../services/marketTrendCourseLinkService';


export const fetchAllMarketTrendCourseLink = createAsyncThunk(
  'marketTrendCourseLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllMarketTrendCourseLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdMarketTrendCourseLink = createAsyncThunk(
  'marketTrendCourseLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getMarketTrendCourseLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createMarketTrendCourseLink = createAsyncThunk(
  'marketTrendCourseLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createMarketTrendCourseLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateMarketTrendCourseLink = createAsyncThunk(
  'marketTrendCourseLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateMarketTrendCourseLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeMarketTrendCourseLink = createAsyncThunk(
  'marketTrendCourseLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteMarketTrendCourseLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const marketTrendCourseLinkSlice = createSlice({
  name: 'marketTrendCourseLink',
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
      .addCase(fetchAllMarketTrendCourseLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllMarketTrendCourseLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllMarketTrendCourseLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdMarketTrendCourseLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdMarketTrendCourseLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdMarketTrendCourseLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createMarketTrendCourseLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createMarketTrendCourseLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createMarketTrendCourseLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateMarketTrendCourseLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateMarketTrendCourseLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateMarketTrendCourseLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeMarketTrendCourseLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeMarketTrendCourseLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeMarketTrendCourseLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = marketTrendCourseLinkSlice.actions;
export default marketTrendCourseLinkSlice.reducer;