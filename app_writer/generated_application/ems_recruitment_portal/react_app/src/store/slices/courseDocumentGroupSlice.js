import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCourseDocumentGroup,
  getCourseDocumentGroupById,
  createCourseDocumentGroup as createCourseDocumentGroupApi,
  updateCourseDocumentGroup as updateCourseDocumentGroupApi,
  deleteCourseDocumentGroup as deleteCourseDocumentGroupApi,
} from '../../services/courseDocumentGroupService';


export const fetchAllCourseDocumentGroup = createAsyncThunk(
  'courseDocumentGroup/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCourseDocumentGroup(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCourseDocumentGroup = createAsyncThunk(
  'courseDocumentGroup/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCourseDocumentGroupById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCourseDocumentGroup = createAsyncThunk(
  'courseDocumentGroup/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCourseDocumentGroupApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCourseDocumentGroup = createAsyncThunk(
  'courseDocumentGroup/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCourseDocumentGroupApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCourseDocumentGroup = createAsyncThunk(
  'courseDocumentGroup/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCourseDocumentGroupApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const courseDocumentGroupSlice = createSlice({
  name: 'courseDocumentGroup',
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
      .addCase(fetchAllCourseDocumentGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCourseDocumentGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCourseDocumentGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCourseDocumentGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCourseDocumentGroup.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCourseDocumentGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCourseDocumentGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCourseDocumentGroup.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCourseDocumentGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCourseDocumentGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCourseDocumentGroup.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.groupId === action.payload.groupId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCourseDocumentGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCourseDocumentGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCourseDocumentGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.groupId !== action.meta.arg);
      })
      .addCase(removeCourseDocumentGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = courseDocumentGroupSlice.actions;
export default courseDocumentGroupSlice.reducer;