import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllFieldOfStudy,
  getFieldOfStudyById,
  createFieldOfStudy as createFieldOfStudyApi,
  updateFieldOfStudy as updateFieldOfStudyApi,
  deleteFieldOfStudy as deleteFieldOfStudyApi,
} from '../../services/fieldOfStudyService';


export const fetchAllFieldOfStudy = createAsyncThunk(
  'fieldOfStudy/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllFieldOfStudy(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdFieldOfStudy = createAsyncThunk(
  'fieldOfStudy/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getFieldOfStudyById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createFieldOfStudy = createAsyncThunk(
  'fieldOfStudy/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createFieldOfStudyApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateFieldOfStudy = createAsyncThunk(
  'fieldOfStudy/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateFieldOfStudyApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeFieldOfStudy = createAsyncThunk(
  'fieldOfStudy/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteFieldOfStudyApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const fieldOfStudySlice = createSlice({
  name: 'fieldOfStudy',
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
      .addCase(fetchAllFieldOfStudy.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllFieldOfStudy.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllFieldOfStudy.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdFieldOfStudy.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdFieldOfStudy.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdFieldOfStudy.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createFieldOfStudy.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createFieldOfStudy.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createFieldOfStudy.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateFieldOfStudy.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateFieldOfStudy.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.fieldOfStudyId === action.payload.fieldOfStudyId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateFieldOfStudy.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeFieldOfStudy.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeFieldOfStudy.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.fieldOfStudyId !== action.meta.arg);
      })
      .addCase(removeFieldOfStudy.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = fieldOfStudySlice.actions;
export default fieldOfStudySlice.reducer;