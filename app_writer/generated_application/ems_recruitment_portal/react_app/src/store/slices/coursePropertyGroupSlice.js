import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCoursePropertyGroup,
  getCoursePropertyGroupById,
  createCoursePropertyGroup as createCoursePropertyGroupApi,
  updateCoursePropertyGroup as updateCoursePropertyGroupApi,
  deleteCoursePropertyGroup as deleteCoursePropertyGroupApi,
} from '../../services/coursePropertyGroupService';


export const fetchAllCoursePropertyGroup = createAsyncThunk(
  'coursePropertyGroup/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCoursePropertyGroup(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCoursePropertyGroup = createAsyncThunk(
  'coursePropertyGroup/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCoursePropertyGroupById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCoursePropertyGroup = createAsyncThunk(
  'coursePropertyGroup/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCoursePropertyGroupApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCoursePropertyGroup = createAsyncThunk(
  'coursePropertyGroup/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCoursePropertyGroupApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCoursePropertyGroup = createAsyncThunk(
  'coursePropertyGroup/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCoursePropertyGroupApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const coursePropertyGroupSlice = createSlice({
  name: 'coursePropertyGroup',
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
      .addCase(fetchAllCoursePropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCoursePropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCoursePropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCoursePropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCoursePropertyGroup.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCoursePropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCoursePropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCoursePropertyGroup.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCoursePropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCoursePropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCoursePropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.groupId === action.payload.groupId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCoursePropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCoursePropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCoursePropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.groupId !== action.meta.arg);
      })
      .addCase(removeCoursePropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = coursePropertyGroupSlice.actions;
export default coursePropertyGroupSlice.reducer;