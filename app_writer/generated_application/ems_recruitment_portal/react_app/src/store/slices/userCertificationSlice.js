import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserCertification,
  getUserCertificationById,
  createUserCertification as createUserCertificationApi,
  updateUserCertification as updateUserCertificationApi,
  deleteUserCertification as deleteUserCertificationApi,
} from '../../services/userCertificationService';


export const fetchAllUserCertification = createAsyncThunk(
  'userCertification/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserCertification(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserCertification = createAsyncThunk(
  'userCertification/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserCertificationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserCertification = createAsyncThunk(
  'userCertification/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserCertificationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserCertification = createAsyncThunk(
  'userCertification/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserCertificationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserCertification = createAsyncThunk(
  'userCertification/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserCertificationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userCertificationSlice = createSlice({
  name: 'userCertification',
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
      .addCase(fetchAllUserCertification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserCertification.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserCertification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserCertification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserCertification.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserCertification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserCertification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserCertification.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserCertification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserCertification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserCertification.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.certificationId === action.payload.certificationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserCertification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserCertification.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserCertification.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.certificationId !== action.meta.arg);
      })
      .addCase(removeUserCertification.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userCertificationSlice.actions;
export default userCertificationSlice.reducer;