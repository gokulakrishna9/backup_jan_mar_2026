import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserSocialLink,
  getUserSocialLinkById,
  createUserSocialLink as createUserSocialLinkApi,
  updateUserSocialLink as updateUserSocialLinkApi,
  deleteUserSocialLink as deleteUserSocialLinkApi,
} from '../../services/userSocialLinkService';


export const fetchAllUserSocialLink = createAsyncThunk(
  'userSocialLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserSocialLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserSocialLink = createAsyncThunk(
  'userSocialLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserSocialLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserSocialLink = createAsyncThunk(
  'userSocialLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserSocialLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserSocialLink = createAsyncThunk(
  'userSocialLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserSocialLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserSocialLink = createAsyncThunk(
  'userSocialLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserSocialLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userSocialLinkSlice = createSlice({
  name: 'userSocialLink',
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
      .addCase(fetchAllUserSocialLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserSocialLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserSocialLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserSocialLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserSocialLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserSocialLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserSocialLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserSocialLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserSocialLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserSocialLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserSocialLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserSocialLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserSocialLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserSocialLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeUserSocialLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userSocialLinkSlice.actions;
export default userSocialLinkSlice.reducer;