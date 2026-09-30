import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllStudentProfile,
  getStudentProfileById,
  createStudentProfile as createStudentProfileApi,
  updateStudentProfile as updateStudentProfileApi,
  deleteStudentProfile as deleteStudentProfileApi,
} from '../../services/studentProfileService';


export const fetchAllStudentProfile = createAsyncThunk(
  'studentProfile/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllStudentProfile(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdStudentProfile = createAsyncThunk(
  'studentProfile/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getStudentProfileById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createStudentProfile = createAsyncThunk(
  'studentProfile/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createStudentProfileApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateStudentProfile = createAsyncThunk(
  'studentProfile/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateStudentProfileApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeStudentProfile = createAsyncThunk(
  'studentProfile/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteStudentProfileApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const studentProfileSlice = createSlice({
  name: 'studentProfile',
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
      .addCase(fetchAllStudentProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllStudentProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllStudentProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdStudentProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdStudentProfile.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdStudentProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createStudentProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createStudentProfile.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createStudentProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateStudentProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateStudentProfile.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.studentProfileId === action.payload.studentProfileId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateStudentProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeStudentProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeStudentProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.studentProfileId !== action.meta.arg);
      })
      .addCase(removeStudentProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = studentProfileSlice.actions;
export default studentProfileSlice.reducer;