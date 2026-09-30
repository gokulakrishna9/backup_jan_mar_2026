import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserInstitutePropertyLink,
  getUserInstitutePropertyLinkById,
  createUserInstitutePropertyLink as createUserInstitutePropertyLinkApi,
  updateUserInstitutePropertyLink as updateUserInstitutePropertyLinkApi,
  deleteUserInstitutePropertyLink as deleteUserInstitutePropertyLinkApi,
} from '../../services/userInstitutePropertyLinkService';


export const fetchAllUserInstitutePropertyLink = createAsyncThunk(
  'userInstitutePropertyLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserInstitutePropertyLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserInstitutePropertyLink = createAsyncThunk(
  'userInstitutePropertyLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserInstitutePropertyLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserInstitutePropertyLink = createAsyncThunk(
  'userInstitutePropertyLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserInstitutePropertyLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserInstitutePropertyLink = createAsyncThunk(
  'userInstitutePropertyLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserInstitutePropertyLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserInstitutePropertyLink = createAsyncThunk(
  'userInstitutePropertyLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserInstitutePropertyLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userInstitutePropertyLinkSlice = createSlice({
  name: 'userInstitutePropertyLink',
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
      .addCase(fetchAllUserInstitutePropertyLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserInstitutePropertyLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserInstitutePropertyLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserInstitutePropertyLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserInstitutePropertyLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserInstitutePropertyLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserInstitutePropertyLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserInstitutePropertyLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserInstitutePropertyLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserInstitutePropertyLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserInstitutePropertyLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserInstitutePropertyLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserInstitutePropertyLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserInstitutePropertyLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeUserInstitutePropertyLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userInstitutePropertyLinkSlice.actions;
export default userInstitutePropertyLinkSlice.reducer;