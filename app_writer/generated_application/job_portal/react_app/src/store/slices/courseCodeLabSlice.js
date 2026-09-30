import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseCodeLab,
  getCourseCodeLabById,
  createCourseCodeLab as createCourseCodeLabApi,
  updateCourseCodeLab as updateCourseCodeLabApi,
  deleteCourseCodeLab as deleteCourseCodeLabApi,
} from '../../services/courseCodeLabService';


export const fetchAllCourseCodeLab = createAsyncThunk(
  'courseCodeLab/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseCodeLab(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseCodeLab = createAsyncThunk(
  'courseCodeLab/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseCodeLabById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseCodeLab = createAsyncThunk(
  'courseCodeLab/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseCodeLabApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseCodeLab = createAsyncThunk(
  'courseCodeLab/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseCodeLabApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseCodeLab = createAsyncThunk(
  'courseCodeLab/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseCodeLabApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseCodeLabSlice = createSlice({
  name: 'courseCodeLab',
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
      .addCase(fetchAllCourseCodeLab.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseCodeLab.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseCodeLab.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseCodeLab.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseCodeLab.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseCodeLab.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseCodeLab.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseCodeLab.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseCodeLab.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseCodeLab.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseCodeLab.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.courseCodeLabId === action.payload.courseCodeLabId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseCodeLab.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseCodeLab.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseCodeLab.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.courseCodeLabId !== action.meta.arg);
      })
      .addCase(removeCourseCodeLab.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseCodeLabSlice.actions;
export default courseCodeLabSlice.reducer;