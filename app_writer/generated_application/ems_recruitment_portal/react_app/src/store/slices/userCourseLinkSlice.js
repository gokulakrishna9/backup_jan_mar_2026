import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserCourseLink,
  getUserCourseLinkById,
  createUserCourseLink as createUserCourseLinkApi,
  updateUserCourseLink as updateUserCourseLinkApi,
  deleteUserCourseLink as deleteUserCourseLinkApi,
} from '../../services/userCourseLinkService';


export const fetchAllUserCourseLink = createAsyncThunk(
  'userCourseLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserCourseLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserCourseLink = createAsyncThunk(
  'userCourseLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserCourseLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserCourseLink = createAsyncThunk(
  'userCourseLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserCourseLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserCourseLink = createAsyncThunk(
  'userCourseLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserCourseLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserCourseLink = createAsyncThunk(
  'userCourseLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserCourseLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userCourseLinkSlice = createSlice({
  name: 'userCourseLink',
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
      .addCase(fetchAllUserCourseLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserCourseLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserCourseLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserCourseLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserCourseLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserCourseLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserCourseLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserCourseLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserCourseLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserCourseLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserCourseLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserCourseLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserCourseLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserCourseLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeUserCourseLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userCourseLinkSlice.actions;
export default userCourseLinkSlice.reducer;