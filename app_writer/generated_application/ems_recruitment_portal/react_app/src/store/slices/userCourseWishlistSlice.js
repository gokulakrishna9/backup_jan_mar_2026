import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserCourseWishlist,
  getUserCourseWishlistById,
  createUserCourseWishlist as createUserCourseWishlistApi,
  updateUserCourseWishlist as updateUserCourseWishlistApi,
  deleteUserCourseWishlist as deleteUserCourseWishlistApi,
} from '../../services/userCourseWishlistService';


export const fetchAllUserCourseWishlist = createAsyncThunk(
  'userCourseWishlist/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserCourseWishlist(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserCourseWishlist = createAsyncThunk(
  'userCourseWishlist/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserCourseWishlistById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserCourseWishlist = createAsyncThunk(
  'userCourseWishlist/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserCourseWishlistApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserCourseWishlist = createAsyncThunk(
  'userCourseWishlist/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserCourseWishlistApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserCourseWishlist = createAsyncThunk(
  'userCourseWishlist/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserCourseWishlistApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userCourseWishlistSlice = createSlice({
  name: 'userCourseWishlist',
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
      .addCase(fetchAllUserCourseWishlist.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserCourseWishlist.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserCourseWishlist.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserCourseWishlist.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserCourseWishlist.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserCourseWishlist.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserCourseWishlist.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserCourseWishlist.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserCourseWishlist.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserCourseWishlist.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserCourseWishlist.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.wishId === action.payload.wishId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserCourseWishlist.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserCourseWishlist.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserCourseWishlist.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.wishId !== action.meta.arg);
      })
      .addCase(removeUserCourseWishlist.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userCourseWishlistSlice.actions;
export default userCourseWishlistSlice.reducer;