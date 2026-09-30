import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllUserAssignmentSubmission,
  getUserAssignmentSubmissionById,
  createUserAssignmentSubmission as createUserAssignmentSubmissionApi,
  updateUserAssignmentSubmission as updateUserAssignmentSubmissionApi,
  deleteUserAssignmentSubmission as deleteUserAssignmentSubmissionApi,
} from '../../services/userAssignmentSubmissionService';


export const fetchAllUserAssignmentSubmission = createAsyncThunk(
  'userAssignmentSubmission/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllUserAssignmentSubmission(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdUserAssignmentSubmission = createAsyncThunk(
  'userAssignmentSubmission/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getUserAssignmentSubmissionById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createUserAssignmentSubmission = createAsyncThunk(
  'userAssignmentSubmission/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createUserAssignmentSubmissionApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateUserAssignmentSubmission = createAsyncThunk(
  'userAssignmentSubmission/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateUserAssignmentSubmissionApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeUserAssignmentSubmission = createAsyncThunk(
  'userAssignmentSubmission/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteUserAssignmentSubmissionApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const userAssignmentSubmissionSlice = createSlice({
  name: 'userAssignmentSubmission',
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
      .addCase(fetchAllUserAssignmentSubmission.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllUserAssignmentSubmission.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllUserAssignmentSubmission.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdUserAssignmentSubmission.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdUserAssignmentSubmission.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdUserAssignmentSubmission.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createUserAssignmentSubmission.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createUserAssignmentSubmission.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createUserAssignmentSubmission.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateUserAssignmentSubmission.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateUserAssignmentSubmission.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.submissionId === action.payload.submissionId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateUserAssignmentSubmission.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeUserAssignmentSubmission.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeUserAssignmentSubmission.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.submissionId !== action.meta.arg);
      })
      .addCase(removeUserAssignmentSubmission.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = userAssignmentSubmissionSlice.actions;
export default userAssignmentSubmissionSlice.reducer;